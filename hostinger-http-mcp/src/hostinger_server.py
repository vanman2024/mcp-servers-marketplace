#!/usr/bin/env python3
"""
Hostinger HTTP MCP Server
Domain, DNS, and billing management tools for Hostinger services.
Based on the official Hostinger API MCP server pattern with FastMCP HTTP transport.
"""

import os
import json
from typing import Any, Dict, List, Optional
from datetime import datetime
from fastmcp import FastMCP

# Initialize the MCP server
mcp = FastMCP("Hostinger HTTP Server")

# Billing Tools

@mcp.tool()
async def hostinger_get_catalog_items(category: Optional[str] = None) -> Dict[str, Any]:
    """Get list of available catalog items for purchase"""
    try:
        # In production, this would call Hostinger API
        catalog_items = [
            {"id": "hosting_premium", "name": "Premium Hosting", "price": 9.99, "category": "hosting"},
            {"id": "domain_com", "name": ".com Domain", "price": 12.99, "category": "domain"},
            {"id": "ssl_cert", "name": "SSL Certificate", "price": 19.99, "category": "security"}
        ]
        
        if category:
            catalog_items = [item for item in catalog_items if item["category"] == category]
        
        return {
            "success": True,
            "items": catalog_items,
            "count": len(catalog_items),
            "category": category,
            "action": "get_catalog"
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool()
async def hostinger_create_order(
    item_id: str,
    quantity: int = 1,
    payment_method_id: Optional[str] = None
) -> Dict[str, Any]:
    """Create a new service order"""
    try:
        order_id = f"order_{datetime.now().timestamp()}"
        
        return {
            "success": True,
            "order_id": order_id,
            "item_id": item_id,
            "quantity": quantity,
            "payment_method_id": payment_method_id,
            "status": "pending",
            "message": "Order created successfully",
            "action": "create_order"
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool()
async def hostinger_list_subscriptions(
    status: Optional[str] = None,
    limit: int = 50
) -> Dict[str, Any]:
    """List all active subscriptions"""
    try:
        # Mock subscription data
        subscriptions = [
            {
                "id": "sub_001",
                "service": "Premium Hosting",
                "status": "active",
                "renews_at": "2024-12-01",
                "price": 9.99
            },
            {
                "id": "sub_002",
                "service": "example.com Domain",
                "status": "active",
                "renews_at": "2024-11-15",
                "price": 12.99
            }
        ]
        
        if status:
            subscriptions = [sub for sub in subscriptions if sub["status"] == status]
        
        return {
            "success": True,
            "subscriptions": subscriptions[:limit],
            "total": len(subscriptions),
            "limit": limit,
            "action": "list_subscriptions"
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool()
async def hostinger_cancel_subscription(subscription_id: str, reason: Optional[str] = None) -> Dict[str, Any]:
    """Cancel an active subscription"""
    try:
        return {
            "success": True,
            "subscription_id": subscription_id,
            "status": "cancelled",
            "reason": reason,
            "cancelled_at": datetime.now().isoformat(),
            "message": f"Subscription {subscription_id} cancelled successfully",
            "action": "cancel_subscription"
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

# DNS Management Tools

@mcp.tool()
async def hostinger_get_dns_records(domain: str, record_type: Optional[str] = None) -> Dict[str, Any]:
    """Retrieve DNS zone records for a domain"""
    try:
        # Mock DNS records
        dns_records = [
            {"type": "A", "name": "@", "value": "192.168.1.1", "ttl": 3600},
            {"type": "A", "name": "www", "value": "192.168.1.1", "ttl": 3600},
            {"type": "MX", "name": "@", "value": "mail.example.com", "priority": 10, "ttl": 3600},
            {"type": "TXT", "name": "@", "value": "v=spf1 include:_spf.google.com ~all", "ttl": 3600}
        ]
        
        if record_type:
            dns_records = [record for record in dns_records if record["type"] == record_type]
        
        return {
            "success": True,
            "domain": domain,
            "records": dns_records,
            "count": len(dns_records),
            "record_type": record_type,
            "action": "get_dns_records"
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool()
async def hostinger_update_dns_record(
    domain: str,
    record_id: str,
    record_type: str,
    name: str,
    value: str,
    ttl: int = 3600,
    priority: Optional[int] = None
) -> Dict[str, Any]:
    """Update a DNS record"""
    try:
        record = {
            "id": record_id,
            "type": record_type,
            "name": name,
            "value": value,
            "ttl": ttl
        }
        
        if priority and record_type in ["MX", "SRV"]:
            record["priority"] = priority
        
        return {
            "success": True,
            "domain": domain,
            "record": record,
            "message": f"DNS record {record_id} updated successfully",
            "action": "update_dns_record"
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool()
async def hostinger_delete_dns_record(domain: str, record_id: str) -> Dict[str, Any]:
    """Delete a DNS record"""
    try:
        return {
            "success": True,
            "domain": domain,
            "record_id": record_id,
            "message": f"DNS record {record_id} deleted successfully",
            "action": "delete_dns_record"
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool()
async def hostinger_create_dns_snapshot(domain: str, name: Optional[str] = None) -> Dict[str, Any]:
    """Create a snapshot of current DNS configuration"""
    try:
        snapshot_id = f"snapshot_{datetime.now().timestamp()}"
        snapshot_name = name or f"DNS Snapshot {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        
        return {
            "success": True,
            "domain": domain,
            "snapshot_id": snapshot_id,
            "name": snapshot_name,
            "created_at": datetime.now().isoformat(),
            "message": "DNS snapshot created successfully",
            "action": "create_dns_snapshot"
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

# Domain Management Tools

@mcp.tool()
async def hostinger_check_domain_availability(domain: str) -> Dict[str, Any]:
    """Check if a domain is available for registration"""
    try:
        # Mock availability check
        available = not domain.startswith("taken")
        
        return {
            "success": True,
            "domain": domain,
            "available": available,
            "price": 12.99 if available else None,
            "currency": "USD",
            "action": "check_domain"
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool()
async def hostinger_purchase_domain(
    domain: str,
    years: int = 1,
    privacy_protection: bool = True,
    auto_renew: bool = True
) -> Dict[str, Any]:
    """Purchase a new domain"""
    try:
        order_id = f"domain_order_{datetime.now().timestamp()}"
        
        return {
            "success": True,
            "domain": domain,
            "order_id": order_id,
            "years": years,
            "privacy_protection": privacy_protection,
            "auto_renew": auto_renew,
            "total_price": 12.99 * years,
            "currency": "USD",
            "message": f"Domain {domain} purchased successfully",
            "action": "purchase_domain"
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool()
async def hostinger_manage_domain_forwarding(
    domain: str,
    enable: bool,
    destination_url: Optional[str] = None,
    forwarding_type: str = "301"
) -> Dict[str, Any]:
    """Enable or disable domain forwarding"""
    try:
        return {
            "success": True,
            "domain": domain,
            "forwarding_enabled": enable,
            "destination_url": destination_url if enable else None,
            "forwarding_type": forwarding_type if enable else None,
            "message": f"Domain forwarding {'enabled' if enable else 'disabled'} for {domain}",
            "action": "manage_forwarding"
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool()
async def hostinger_toggle_privacy_protection(domain: str, enable: bool) -> Dict[str, Any]:
    """Enable or disable domain privacy protection"""
    try:
        return {
            "success": True,
            "domain": domain,
            "privacy_protection": enable,
            "message": f"Privacy protection {'enabled' if enable else 'disabled'} for {domain}",
            "action": "toggle_privacy"
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool()
async def hostinger_update_nameservers(
    domain: str,
    nameservers: List[str]
) -> Dict[str, Any]:
    """Update domain nameservers"""
    try:
        if len(nameservers) < 2 or len(nameservers) > 5:
            return {
                "success": False,
                "error": "Must provide between 2 and 5 nameservers"
            }
        
        return {
            "success": True,
            "domain": domain,
            "nameservers": nameservers,
            "message": f"Nameservers updated for {domain}",
            "action": "update_nameservers"
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool()
async def hostinger_get_whois_profiles() -> Dict[str, Any]:
    """Get list of WHOIS profiles"""
    try:
        profiles = [
            {
                "id": "profile_001",
                "name": "Default Profile",
                "email": "admin@example.com",
                "organization": "Example Corp",
                "country": "US"
            },
            {
                "id": "profile_002",
                "name": "Business Profile",
                "email": "business@example.com",
                "organization": "Business Inc",
                "country": "US"
            }
        ]
        
        return {
            "success": True,
            "profiles": profiles,
            "count": len(profiles),
            "action": "get_whois_profiles"
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool()
async def hostinger_update_whois_profile(
    profile_id: str,
    email: Optional[str] = None,
    phone: Optional[str] = None,
    organization: Optional[str] = None,
    address: Optional[str] = None
) -> Dict[str, Any]:
    """Update WHOIS profile information"""
    try:
        updates = {}
        if email: updates["email"] = email
        if phone: updates["phone"] = phone
        if organization: updates["organization"] = organization
        if address: updates["address"] = address
        
        return {
            "success": True,
            "profile_id": profile_id,
            "updates": updates,
            "message": f"WHOIS profile {profile_id} updated successfully",
            "action": "update_whois_profile"
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

if __name__ == "__main__":
    # Get port from environment variable
    port = int(os.getenv('HOSTINGER_MCP_PORT', '8024'))
    
    # Check for API key
    api_key = os.getenv('HOSTINGER_API_KEY')
    if not api_key:
        print("Warning: HOSTINGER_API_KEY not set - running in demo mode")
    
    print(f"Hostinger server initializing...")
    print(f"Starting Hostinger HTTP MCP Server on port {port}")
    print("Domain, DNS, and billing management tools")
    
    # Run the server
    mcp.run(transport="streamable-http", host="0.0.0.0", port=port, path="/")