#!/usr/bin/env python3
"""
Comprehensive testing and validation script for the entire project.
"""

import os
import sys
import subprocess
import requests
import json
from pathlib import Path
from time import sleep

# Color codes for output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

class ProjectValidator:
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.warnings = 0
        self.base_url = "http://localhost:8000"
        self.frontend_url = "http://localhost:3000"
        self.test_user = {
            "name": "Test User",
            "email": "test@example.com",
            "password": "test123456"
        }
        self.auth_token = None
    
    def print_header(self, title):
        print(f"\n{BLUE}{'='*60}")
        print(f"{title:^60}")
        print(f"{'='*60}{RESET}\n")
    
    def print_test(self, name, passed, message=""):
        status = f"{GREEN}✅ PASS{RESET}" if passed else f"{RED}❌ FAIL{RESET}"
        print(f"  {status} | {name}")
        if message:
            print(f"        {message}")
        if passed:
            self.passed += 1
        else:
            self.failed += 1
    
    def print_warning(self, message):
        print(f"  {YELLOW}⚠️  {message}{RESET}")
        self.warnings += 1
    
    def check_health(self):
        """Test backend health endpoint"""
        self.print_header("Backend Health Checks")
        
        try:
            response = requests.get(f"{self.base_url}/health", timeout=5)
            if response.status_code == 200:
                data = response.json()
                self.print_test("Health check endpoint", True, f"Status: {data.get('status')}")
            else:
                self.print_test("Health check endpoint", False, f"Status code: {response.status_code}")
        except Exception as e:
            self.print_test("Backend connectivity", False, f"Error: {str(e)}")
            self.print_warning("Backend appears to be down. Start with: python backend/run.bat")
            return False
        
        return True
    
    def check_api_endpoints(self):
        """Test that all API endpoints are accessible"""
        self.print_header("API Endpoint Validation")
        
        endpoints = [
            ("GET", "/"),
            ("GET", "/docs"),
            ("POST", "/api/auth/register"),
            ("POST", "/api/auth/login"),
        ]
        
        for method, endpoint in endpoints:
            try:
                if method == "GET":
                    response = requests.get(f"{self.base_url}{endpoint}", timeout=5)
                else:
                    response = requests.post(f"{self.base_url}{endpoint}", json={}, timeout=5)
                
                # 404 means endpoint doesn't exist, others are OK (401, 422, etc.)
                passed = response.status_code != 404
                self.print_test(f"{method} {endpoint}", passed, f"Status: {response.status_code}")
            except Exception as e:
                self.print_test(f"{method} {endpoint}", False, str(e))
    
    def test_authentication(self):
        """Test user registration and login flow"""
        self.print_header("Authentication Flow")
        
        # Test registration
        try:
            response = requests.post(
                f"{self.base_url}/api/auth/register",
                json=self.test_user,
                timeout=5
            )
            self.print_test("User registration", response.status_code in [200, 201], 
                          f"Status: {response.status_code}")
        except Exception as e:
            self.print_test("User registration", False, str(e))
            return
        
        # Test login
        try:
            response = requests.post(
                f"{self.base_url}/api/auth/login",
                json={
                    "email": self.test_user["email"],
                    "password": self.test_user["password"]
                },
                timeout=5
            )
            if response.status_code == 200:
                data = response.json()
                self.auth_token = data.get("access_token")
                self.print_test("User login", True, "Token obtained")
            else:
                self.print_test("User login", False, f"Status: {response.status_code}")
        except Exception as e:
            self.print_test("User login", False, str(e))
    
    def test_authenticated_endpoints(self):
        """Test endpoints that require authentication"""
        self.print_header("Authenticated Endpoint Tests")
        
        if not self.auth_token:
            self.print_warning("Skipping authenticated tests (no token)")
            return
        
        headers = {"Authorization": f"Bearer {self.auth_token}"}
        
        endpoints = [
            ("GET", "/api/dashboard"),
            ("GET", "/api/resume/analysis"),
            ("GET", "/api/internships"),
            ("GET", "/api/career/recommendations"),
        ]
        
        for method, endpoint in endpoints:
            try:
                if method == "GET":
                    response = requests.get(f"{self.base_url}{endpoint}", headers=headers, timeout=5)
                else:
                    response = requests.post(f"{self.base_url}{endpoint}", headers=headers, json={}, timeout=5)
                
                # Success if not 401 or 404
                passed = response.status_code not in [401, 404, 403]
                self.print_test(f"{method} {endpoint}", passed, f"Status: {response.status_code}")
            except Exception as e:
                self.print_test(f"{method} {endpoint}", False, str(e))
    
    def test_frontend(self):
        """Test frontend accessibility"""
        self.print_header("Frontend Validation")
        
        try:
            response = requests.get(self.frontend_url, timeout=5)
            self.print_test("Frontend accessibility", response.status_code == 200, 
                          f"Status: {response.status_code}")
        except Exception as e:
            self.print_test("Frontend accessibility", False, str(e))
            self.print_warning("Frontend appears to be down. Start with: npm run dev")
        
        # Check key pages
        pages = ["/", "/login", "/register", "/dashboard"]
        for page in pages:
            try:
                response = requests.get(f"{self.frontend_url}{page}", timeout=5, allow_redirects=True)
                self.print_test(f"Page: {page}", response.status_code == 200, 
                              f"Status: {response.status_code}")
            except Exception as e:
                self.print_test(f"Page: {page}", False, str(e))
    
    def test_database(self):
        """Test database connectivity through API"""
        self.print_header("Database Validation")
        
        # Try to query users (requires auth)
        if self.auth_token:
            try:
                headers = {"Authorization": f"Bearer {self.auth_token}"}
                response = requests.get(f"{self.base_url}/api/internships", headers=headers, timeout=5)
                self.print_test("Database query", response.status_code in [200, 401], 
                              f"Status: {response.status_code}")
            except Exception as e:
                self.print_test("Database query", False, str(e))
        else:
            self.print_warning("Database test skipped (no authentication token)")
    
    def test_cors(self):
        """Test CORS configuration"""
        self.print_header("CORS Configuration")
        
        try:
            response = requests.options(
                f"{self.base_url}/api/auth/login",
                headers={
                    "Origin": self.frontend_url,
                    "Access-Control-Request-Method": "POST",
                    "Access-Control-Request-Headers": "Content-Type",
                },
                timeout=5
            )
            
            cors_headers = response.headers
            has_cors = "access-control-allow-origin" in cors_headers
            self.print_test("CORS headers", has_cors, 
                          f"Allow-Origin: {cors_headers.get('access-control-allow-origin', 'Not set')}")
        except Exception as e:
            self.print_test("CORS check", False, str(e))
    
    def check_files(self):
        """Check if all required files exist"""
        self.print_header("Required Files Check")
        
        required_files = {
            "Backend": [
                "backend/app/main.py",
                "backend/app/core/config.py",
                "backend/app/core/security.py",
                "backend/app/core/deps.py",
                "backend/app/db/models.py",
                "backend/app/api/auth.py",
                "backend/requirements.txt",
                "backend/.env",
            ],
            "Frontend": [
                "frontend/app/page.tsx",
                "frontend/app/layout.tsx",
                "frontend/app/login/page.tsx",
                "frontend/next.config.js",
                "frontend/tsconfig.json",
                "frontend/package.json",
                "frontend/.env.local",
                "frontend/public/favicon.svg",
            ],
            "Root": [
                "docker-compose.yml",
                "README.md",
                "SETUP.md",
                ".gitignore",
            ]
        }
        
        for category, files in required_files.items():
            print(f"\n  {category}:")
            for file_path in files:
                exists = Path(file_path).exists()
                status = f"{GREEN}✅{RESET}" if exists else f"{RED}❌{RESET}"
                print(f"    {status} {file_path}")
                if exists:
                    self.passed += 1
                else:
                    self.failed += 1
    
    def generate_summary(self):
        """Generate test summary"""
        self.print_header("Test Summary")
        
        total = self.passed + self.failed
        percentage = (self.passed / total * 100) if total > 0 else 0
        
        print(f"  {GREEN}✅ Passed: {self.passed}{RESET}")
        print(f"  {RED}❌ Failed: {self.failed}{RESET}")
        print(f"  {YELLOW}⚠️  Warnings: {self.warnings}{RESET}")
        print(f"\n  Total Tests: {total}")
        print(f"  Success Rate: {percentage:.1f}%")
        
        if self.failed == 0 and self.passed > 0:
            print(f"\n  {GREEN}🎉 All tests passed!{RESET}")
            print(f"  The application is ready for testing.")
        elif self.failed > 0:
            print(f"\n  {RED}⚠️  Some tests failed.{RESET}")
            print(f"  Please review the errors above.")
    
    def run_all_checks(self):
        """Run all validation checks"""
        print(f"{BLUE}")
        print("╔═══════════════════════════════════════════════════════════╗")
        print("║  AI Internship & Placement Intelligence Platform          ║")
        print("║  Comprehensive Project Validation                         ║")
        print("╚═══════════════════════════════════════════════════════════╝")
        print(f"{RESET}")
        
        # Check files first
        self.check_files()
        
        # Only proceed with network tests if backend is reachable
        if not self.check_health():
            print(f"\n{RED}Backend is not accessible. Please start the backend server.{RESET}")
            self.generate_summary()
            return False
        
        self.check_api_endpoints()
        self.test_authentication()
        self.test_authenticated_endpoints()
        self.test_database()
        self.test_cors()
        self.test_frontend()
        
        self.generate_summary()
        return self.failed == 0


if __name__ == "__main__":
    validator = ProjectValidator()
    success = validator.run_all_checks()
    sys.exit(0 if success else 1)
