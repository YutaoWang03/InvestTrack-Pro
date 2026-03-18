#!/usr/bin/env python3
"""
Core calculation functions for investment metrics
Based on the algorithm documentation in docs/相关算法说明文档.md
"""

from decimal import Decimal
import math
from typing import List, Tuple

def calc_holding_period_return(current_price: Decimal, avg_cost: Decimal) -> Decimal:
    """
    Calculate holding period return
    Formula: (current_price - avg_cost) / avg_cost
    
    Args:
        current_price: Current price of the security
        avg_cost: Average cost of the position
        
    Returns:
        Holding period return as a decimal
    """
    if avg_cost == 0:
        return Decimal('0')
    
    return (current_price - avg_cost) / avg_cost

def calc_dynamic_annualized_return(holding_return: Decimal, days_held: int) -> Decimal:
    """
    Calculate dynamic annualized return
    Formula: (1 + holding_return) ^ (250 / days_held) - 1
    
    Args:
        holding_return: Holding period return
        days_held: Number of days held
        
    Returns:
        Annualized return as a decimal
    """
    if days_held == 0:
        return Decimal('0')
    
    # Convert to float for calculation, then back to Decimal
    holding_return_float = float(holding_return)
    
    # Handle edge case where holding_return is -1
    if holding_return_float <= -1:
        return Decimal('-1')
    
    # Ensure the exponent is a float
    exponent = 250 / days_held
    annualized = (1 + holding_return_float) ** exponent - 1
    
    # Handle NaN or Infinity
    if not isinstance(annualized, (int, float)) or annualized != annualized:  # Check for NaN
        return Decimal('0')
    
    # Convert to string with limited decimal places to avoid conversion issues
    return Decimal(str(round(annualized, 10)))

def calc_volatility(prices: List[Decimal]) -> Decimal:
    """
    Calculate annualized volatility
    Formula: sqrt( (1/(N-1)) * sum((r_i - avg_r)^2) ) * sqrt(250)
    
    Args:
        prices: List of closing prices
        
    Returns:
        Annualized volatility as a decimal
    """
    if len(prices) < 2:
        return Decimal('0')
    
    # Calculate daily returns
    returns = []
    for i in range(1, len(prices)):
        if prices[i-1] == 0:
            continue
        daily_return = (prices[i] - prices[i-1]) / prices[i-1]
        returns.append(daily_return)
    
    if len(returns) < 2:
        return Decimal('0')
    
    # Calculate average return
    avg_return = sum(returns) / Decimal(str(len(returns)))
    
    # Calculate variance
    variance = sum((r - avg_return) ** 2 for r in returns) / Decimal(str(len(returns) - 1))
    
    # Calculate standard deviation (volatility)
    volatility = Decimal(str(math.sqrt(float(variance))))
    
    # Annualize (250 trading days)
    annualized_volatility = volatility * Decimal(str(math.sqrt(250)))
    
    return annualized_volatility

def calc_sharpe_ratio(annualized_return: Decimal, volatility: Decimal, risk_free_rate: Decimal = Decimal('0.015')) -> Decimal:
    """
    Calculate Sharpe ratio
    Formula: (annualized_return - risk_free_rate) / volatility
    
    Args:
        annualized_return: Annualized return of the portfolio
        volatility: Annualized volatility of the portfolio
        risk_free_rate: Risk-free rate (default: 1.5%)
        
    Returns:
        Sharpe ratio as a decimal
    """
    if volatility == 0:
        return Decimal('0')
    
    return (annualized_return - risk_free_rate) / volatility

def calc_max_drawdown(prices: List[Decimal]) -> Decimal:
    """
    Calculate maximum drawdown
    Formula: (peak_price - trough_price) / peak_price
    
    Args:
        prices: List of closing prices
        
    Returns:
        Maximum drawdown as a decimal (positive value)
    """
    if len(prices) < 2:
        return Decimal('0')
    
    max_drawdown = Decimal('0')
    peak = prices[0]
    
    for price in prices[1:]:
        if price > peak:
            peak = price
        else:
            drawdown = (peak - price) / peak
            if drawdown > max_drawdown:
                max_drawdown = drawdown
    
    return max_drawdown

def calc_var_historical(portfolio_value: Decimal, volatility: Decimal, confidence_level: float = 0.95) -> Decimal:
    """
    Calculate Value at Risk (VaR) using historical method
    Formula: portfolio_value * (z_score * volatility)
    
    Args:
        portfolio_value: Total portfolio value
        volatility: Annualized volatility
        confidence_level: Confidence level (default: 95%)
        
    Returns:
        VaR as a decimal
    """
    # Z-score for different confidence levels
    z_scores = {
        0.90: 1.28,
        0.95: 1.645,
        0.99: 2.33
    }
    
    z_score = Decimal(str(z_scores.get(confidence_level, 1.645)))
    
    # Calculate daily volatility (divide by sqrt(250))
    daily_volatility = volatility / Decimal(str(math.sqrt(250)))
    
    # Calculate VaR
    var = portfolio_value * z_score * daily_volatility
    
    return var

def calc_cvar_historical(returns: List[Decimal], var: Decimal) -> Decimal:
    """
    Calculate Conditional Value at Risk (CVaR)
    Formula: Average of returns that are less than -VaR
    
    Args:
        returns: List of returns
        var: Value at Risk
        
    Returns:
        CVaR as a decimal
    """
    # Filter returns that are below -VaR
    extreme_losses = [r for r in returns if r < -var]
    
    if not extreme_losses:
        return Decimal('0')
    
    # Calculate average of extreme losses
    cvar = sum(extreme_losses) / Decimal(str(len(extreme_losses)))
    
    return abs(cvar)  # Return as positive value

def calc_bias(current_price: Decimal, ma20: Decimal) -> Decimal:
    """
    Calculate bias ratio (for right-side trading)
    Formula: (current_price - ma20) / ma20 * 100
    
    Args:
        current_price: Current price of the security
        ma20: 20-day moving average
        
    Returns:
        Bias ratio as a decimal (percentage)
    """
    if ma20 == 0:
        return Decimal('0')
    
    bias = (current_price - ma20) / ma20 * Decimal('100')
    return bias

def calc_atr(highs: List[Decimal], lows: List[Decimal], closes: List[Decimal], period: int = 20) -> Decimal:
    """
    Calculate Average True Range (ATR)
    
    Args:
        highs: List of high prices
        lows: List of low prices
        closes: List of closing prices
        period: ATR calculation period (default: 20)
        
    Returns:
        ATR as a decimal
    """
    if len(highs) < period or len(lows) < period or len(closes) < period:
        return Decimal('0')
    
    true_ranges = []
    
    # Calculate true range for each day
    for i in range(1, len(highs)):
        high_low = highs[i] - lows[i]
        high_prev_close = abs(highs[i] - closes[i-1])
        low_prev_close = abs(lows[i] - closes[i-1])
        
        true_range = max(high_low, high_prev_close, low_prev_close)
        true_ranges.append(true_range)
    
    if len(true_ranges) < period:
        return Decimal('0')
    
    # Calculate ATR as the average of true ranges
    atr = sum(true_ranges[-period:]) / Decimal(str(period))
    
    return atr

def calc_stop_loss(avg_cost: Decimal, atr: Decimal, multiplier: Decimal = Decimal('2.0')) -> Decimal:
    """
    Calculate stop loss price
    Formula: avg_cost - (atr * multiplier)
    
    Args:
        avg_cost: Average cost of the position
        atr: Average True Range
        multiplier: ATR multiplier for stop loss (default: 2.0)
        
    Returns:
        Stop loss price as a decimal
    """
    stop_loss_price = avg_cost - (atr * multiplier)
    
    # Ensure stop loss price is not negative
    if stop_loss_price < Decimal('0'):
        stop_loss_price = Decimal('0')
    
    return stop_loss_price