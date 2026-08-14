#!/usr/bin/env python3
"""
FastAPI Backend for LayanSociety Economic Analysis Platform
Provides REST API endpoints for all economic calculators.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from pydantic import BaseModel
from typing import List, Optional
import sys
import os
from datetime import datetime
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT

# Import core modules (now in same directory)
from tunisia_inflation_calculator import calculate_inflation, INFLATION_RATES
from tunisia_future_cost_estimator import estimate_future_cost, ENVIRONMENTAL_SURCHARGES
from tunisia_economic_indicators import (
    calculate_gdp_projection,
    calculate_unemployment_impact,
    calculate_currency_conversion,
    calculate_interest_impact,
    get_economic_summary,
)

app = FastAPI(
    title="LayanSociety API",
    description="Economic Analysis and Cost Calculation API",
    version="1.0.0"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Root endpoint for health checks
@app.get("/")
async def root():
    """Health check endpoint."""
    return {"status": "healthy", "message": "LayanSociety API is running"}


# Pydantic models for request/response
class InflationRequest(BaseModel):
    amount: float
    base_year: int
    additional_costs: Optional[List[dict]] = None


class InflationResponse(BaseModel):
    original_amount: float
    base_year: int
    adjusted_amount: float
    multiplier: float
    additional_costs_adjusted: Optional[List[dict]] = None
    grand_total: Optional[float] = None


class FutureCostRequest(BaseModel):
    amount: float
    base_year: int
    target_year: int
    category: str = "general"
    scenario: str = "baseline"


class GDPRequest(BaseModel):
    initial_gdp: float
    start_year: int
    target_year: int
    scenario: str = "baseline"


class UnemploymentRequest(BaseModel):
    initial_rate: float
    start_year: int
    target_year: int
    scenario: str = "baseline"


class CurrencyRequest(BaseModel):
    amount: float
    from_currency: str
    to_currency: str
    year: int


class InterestRequest(BaseModel):
    principal: float
    years: int
    start_year: int
    scenario: str = "baseline"


class ReportRequest(BaseModel):
    report_type: str  # 'inflation', 'gdp', 'unemployment', 'currency', 'interest', 'future_cost'
    data: dict
    username: str = "Client"
    account_number: str = ""


# API Endpoints
@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "name": "LayanSociety API",
        "version": "1.0.0",
        "description": "Economic Analysis and Cost Calculation API",
        "endpoints": {
            "inflation": "/api/inflation",
            "future_cost": "/api/future-cost",
            "gdp": "/api/gdp",
            "unemployment": "/api/unemployment",
            "currency": "/api/currency",
            "interest": "/api/interest",
            "economic_summary": "/api/economic-summary/{year}"
        }
    }


@app.get("/api/inflation-rates")
async def get_inflation_rates():
    """Get all available inflation rates."""
    return INFLATION_RATES


@app.get("/api/economic-summary/{year}")
async def get_economic_summary_endpoint(year: int):
    """Get economic summary for a specific year."""
    try:
        return get_economic_summary(year)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/api/inflation", response_model=InflationResponse)
async def calculate_inflation_endpoint(request: InflationRequest):
    """Calculate inflation adjustment."""
    try:
        adjusted_amount = calculate_inflation(request.amount, request.base_year)
        multiplier = adjusted_amount / request.amount if request.amount != 0 else 0
        
        response = InflationResponse(
            original_amount=request.amount,
            base_year=request.base_year,
            adjusted_amount=adjusted_amount,
            multiplier=multiplier
        )
        
        if request.additional_costs:
            from tunisia_inflation_calculator import _total_adjusted_additional_costs
            total_additional_adjusted = _total_adjusted_additional_costs(request.additional_costs)
            response.additional_costs_adjusted = request.additional_costs
            response.grand_total = adjusted_amount + total_additional_adjusted
        
        return response
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/api/future-cost")
async def calculate_future_cost_endpoint(request: FutureCostRequest):
    """Calculate future cost projection."""
    try:
        result = estimate_future_cost(
            amount=request.amount,
            base_year=request.base_year,
            target_year=request.target_year,
            category=request.category,
            scenario=request.scenario
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/api/gdp")
async def calculate_gdp_endpoint(request: GDPRequest):
    """Calculate GDP projection."""
    try:
        result = calculate_gdp_projection(
            initial_gdp=request.initial_gdp,
            start_year=request.start_year,
            target_year=request.target_year,
            scenario=request.scenario
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/api/unemployment")
async def calculate_unemployment_endpoint(request: UnemploymentRequest):
    """Calculate unemployment projection."""
    try:
        result = calculate_unemployment_impact(
            initial_rate=request.initial_rate,
            start_year=request.start_year,
            target_year=request.target_year,
            scenario=request.scenario
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/api/currency")
async def calculate_currency_endpoint(request: CurrencyRequest):
    """Calculate currency conversion."""
    try:
        result = calculate_currency_conversion(
            amount=request.amount,
            from_currency=request.from_currency,
            to_currency=request.to_currency,
            year=request.year
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/api/interest")
async def calculate_interest_endpoint(request: InterestRequest):
    """Calculate interest impact."""
    try:
        result = calculate_interest_impact(
            principal=request.principal,
            years=request.years,
            start_year=request.start_year,
            scenario=request.scenario
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


def generate_pdf_report(report_type: str, data: dict, username: str, account_number: str) -> bytes:
    """Generate a professional PDF report."""
    from io import BytesIO
    
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)
    
    # Custom styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor("#5B38AB"),
        spaceAfter=30,
        alignment=TA_CENTER
    )
    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#4A5568'),
        spaceAfter=20,
        alignment=TA_CENTER
    )
    header_style = ParagraphStyle(
        'CustomHeader',
        parent=styles['Heading3'],
        fontSize=12,
        textColor=colors.HexColor('#2D3748'),
        spaceAfter=12,
        spaceBefore=20
    )
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.HexColor('#4A5568'),
        spaceAfter=10
    )
    
    story = []
    
    # Header
    story.append(Paragraph("LAYAN SOCIETY FOR COST CALCULATION", title_style))
    story.append(Paragraph("AND RISK ESTIMATION", title_style))
    story.append(Spacer(1, 0.2*inch))
    
    # Report title based on type
    report_titles = {
        'inflation': 'INFLATION ADJUSTMENT REPORT',
        'gdp': 'GDP PROJECTION REPORT',
        'unemployment': 'UNEMPLOYMENT RATE PROJECTION REPORT',
        'currency': 'CURRENCY CONVERSION REPORT',
        'interest': 'INTEREST RATE IMPACT REPORT',
        'future_cost': 'FUTURE COST PROJECTION REPORT'
    }
    
    story.append(Paragraph(report_titles.get(report_type, 'ECONOMIC ANALYSIS REPORT'), ParagraphStyle(
        'ReportTitle',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#2D3748'),
        spaceAfter=20,
        alignment=TA_CENTER
    )))
    story.append(Spacer(1, 0.1*inch))
    
    # Client information
    story.append(Paragraph("CLIENT INFORMATION", header_style))
    client_data = [
        ['Account Holder:', username],
        ['Account Number:', account_number or 'N/A'],
        ['Report Date:', datetime.now().strftime('%d/%m/%Y %H:%M:%S')],
        ['Report Type:', report_type.upper()]
    ]
    
    client_table = Table(client_data, colWidths=[2*inch, 4*inch])
    client_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#F7FAFC')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E2E8F0')),
    ]))
    story.append(client_table)
    story.append(Spacer(1, 0.2*inch))
    
    # Report content based on type
    if report_type == 'inflation':
        story.append(Paragraph("INFLATION ANALYSIS RESULTS", header_style))
        
        results_data = [
            ['Original Amount:', f"{data.get('original_amount', 0):,.2f} TND"],
            ['Base Year:', str(data.get('base_year', ''))],
            ['Adjusted Amount (2026):', f"{data.get('adjusted_amount', 0):,.2f} TND"],
            ['Value Multiplier:', f"{data.get('multiplier', 0):.2f}x"],
            ['Purchasing Power Loss:', f"{((data.get('multiplier', 1) - 1) * 100):.2f}%"]
        ]
        
        results_table = Table(results_data, colWidths=[2.5*inch, 3.5*inch])
        results_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#F7FAFC')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E2E8F0')),
        ]))
        story.append(results_table)
        
        if data.get('additional_costs_adjusted'):
            story.append(Spacer(1, 0.2*inch))
            story.append(Paragraph("ADDITIONAL COSTS", header_style))
            story.append(Paragraph("Additional costs have been included in this calculation.", normal_style))
        
    elif report_type == 'gdp':
        story.append(Paragraph("GDP PROJECTION RESULTS", header_style))
        
        results_data = [
            ['Initial GDP:', f"{data.get('initial_gdp', 0):,.2f} TND"],
            ['Base Year:', str(data.get('start_year', ''))],
            ['Target Year:', str(data.get('target_year', ''))],
            ['Scenario:', data.get('scenario', '').upper()],
            ['Projected GDP:', f"{data.get('projected_gdp', 0):,.2f} TND"],
            ['Total Growth:', f"{data.get('total_growth_percent', 0):.2f}%"],
            ['Average Annual Growth:', f"{data.get('average_annual_growth', 0):.2f}%"]
        ]
        
        results_table = Table(results_data, colWidths=[2.5*inch, 3.5*inch])
        results_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#F7FAFC')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E2E8F0')),
        ]))
        story.append(results_table)
        
    elif report_type == 'unemployment':
        story.append(Paragraph("UNEMPLOYMENT PROJECTION RESULTS", header_style))
        
        results_data = [
            ['Initial Rate:', f"{data.get('initial_rate', 0):.2f}%"],
            ['Base Year:', str(data.get('start_year', ''))],
            ['Target Year:', str(data.get('target_year', ''))],
            ['Scenario:', data.get('scenario', '').upper()],
            ['Projected Rate:', f"{data.get('projected_rate', 0):.2f}%"],
            ['Total Change:', f"{data.get('total_change', 0):+.2f}%"],
            ['Annual Change:', f"{data.get('annual_change', 0):.3f}%"]
        ]
        
        results_table = Table(results_data, colWidths=[2.5*inch, 3.5*inch])
        results_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#F7FAFC')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E2E8F0')),
        ]))
        story.append(results_table)
        
    elif report_type == 'currency':
        story.append(Paragraph("CURRENCY CONVERSION RESULTS", header_style))
        
        results_data = [
            ['Amount:', f"{data.get('amount', 0):,.2f} {data.get('from_currency', '')}"],
            ['From Currency:', data.get('from_currency', '')],
            ['To Currency:', data.get('to_currency', '')],
            ['Year:', str(data.get('year', ''))],
            ['Exchange Rate:', f"{data.get('exchange_rate', 0):.4f}"],
            ['Converted Amount:', f"{data.get('converted_amount', 0):,.2f} {data.get('to_currency', '')}"]
        ]
        
        results_table = Table(results_data, colWidths=[2.5*inch, 3.5*inch])
        results_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#F7FAFC')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E2E8F0')),
        ]))
        story.append(results_table)
        
    elif report_type == 'interest':
        story.append(Paragraph("INTEREST RATE IMPACT RESULTS", header_style))
        
        results_data = [
            ['Principal:', f"{data.get('principal', 0):,.2f} TND"],
            ['Duration:', f"{data.get('years', 0)} years"],
            ['Start Year:', str(data.get('start_year', ''))],
            ['Scenario:', data.get('scenario', '').upper()],
            ['Average Rate:', f"{data.get('average_rate', 0):.2f}%"],
            ['Final Amount:', f"{data.get('final_amount', 0):,.2f} TND"],
            ['Total Interest:', f"{data.get('total_interest', 0):,.2f} TND"],
            ['Interest Percentage:', f"{data.get('interest_percentage', 0):.2f}%"]
        ]
        
        results_table = Table(results_data, colWidths=[2.5*inch, 3.5*inch])
        results_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#F7FAFC')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E2E8F0')),
        ]))
        story.append(results_table)
        
    elif report_type == 'future_cost':
        story.append(Paragraph("FUTURE COST PROJECTION RESULTS", header_style))
        
        category_label = ENVIRONMENTAL_SURCHARGES.get(data.get('category', 'general'), {}).get('label', 'General')
        
        results_data = [
            ['Original Amount:', f"{data.get('original_amount', 0):,.2f} TND"],
            ['Base Year:', str(data.get('base_year', ''))],
            ['Target Year:', str(data.get('target_year', ''))],
            ['Category:', category_label],
            ['Scenario:', data.get('scenario', '').upper()],
            ['Adjusted (2026):', f"{data.get('adjusted_2026', 0):,.2f} TND"],
            ['Projected Amount:', f"{data.get('projected', 0):,.2f} TND"],
            ['Total Multiplier:', f"{data.get('total_multiplier', 0):.2f}x"],
            ['Annual Rate Used:', f"{data.get('annual_rate_used', 0):.2f}%"]
        ]
        
        results_table = Table(results_data, colWidths=[2.5*inch, 3.5*inch])
        results_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#F7FAFC')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E2E8F0')),
        ]))
        story.append(results_table)
    
    # Disclaimer
    story.append(Spacer(1, 0.3*inch))
    story.append(Paragraph("DISCLAIMER", header_style))
    disclaimer_text = """
    This report is generated by LayanSociety for Cost Calculation and Risk Estimation based on 
    historical economic data from Tunisia. The calculations use official inflation rates, GDP data, 
    unemployment statistics, exchange rates, and interest rates from the Central Bank of Tunisia, 
    World Bank, IMF, and National Statistics Institute (INS).
    
    This document is for informational purposes only and should not be used for official transactions 
    without verification from authorized financial institutions. Projections are based on historical 
    trends and scenarios, and actual results may vary.
    """
    story.append(Paragraph(disclaimer_text, normal_style))
    
    # Footer
    story.append(Spacer(1, 0.2*inch))
    story.append(Paragraph("© 2026 LayanSociety for Cost Calculation and Risk Estimation", ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=8,
        textColor=colors.HexColor('#718096'),
        alignment=TA_CENTER
    )))
    
    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()


@app.post("/api/generate-report")
async def generate_report_endpoint(request: ReportRequest):
    """Generate a professional PDF report."""
    try:
        pdf_bytes = generate_pdf_report(
            report_type=request.report_type,
            data=request.data,
            username=request.username,
            account_number=request.account_number
        )
        
        filename = f"{request.report_type}_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        
        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename={filename}"
            }
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
