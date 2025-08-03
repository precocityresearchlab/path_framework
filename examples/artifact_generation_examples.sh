#!/bin/bash
"""
PATH Framework Artifact Generation Examples
Demonstrates various ways to generate artifacts using UV
"""

echo "🎯 PATH Framework Artifact Generation Examples"
echo "=============================================="
echo ""

echo "1️⃣  Basic Example - Simple API Project"
echo "uv run python path_generate.py --project 'Simple API' --domain business"
echo ""

echo "2️⃣  Detailed Example - E-commerce Platform"
echo "uv run python path_generate.py \\"
echo "  --project 'E-commerce Platform' \\"
echo "  --domain business \\"
echo "  --requirements 'Online shopping with product catalog, cart, checkout, and payment processing' \\"
echo "  --constraints 'Handle 10,000 concurrent users, 99.9% uptime, PCI DSS compliance' \\"
echo "  --stakeholders 'Customers, Store Managers, Payment Processors, Support Staff' \\"
echo "  --compliance 'PCI DSS, GDPR, SOX'"
echo ""

echo "3️⃣  Financial Example - Trading System"
echo "uv run python path_generate.py \\"
echo "  --project 'High-Frequency Trading' \\"
echo "  --domain financial \\"
echo "  --requirements 'Real-time market data processing, algorithmic trading, risk management' \\"
echo "  --constraints 'Sub-millisecond latency, 99.99% uptime, handle 1M transactions/day' \\"
echo "  --stakeholders 'Traders, Risk Managers, Compliance Officers, Market Data Providers' \\"
echo "  --compliance 'FIX 4.4, MiFID II, SOX, Basel III'"
echo ""

echo "4️⃣  Healthcare Example - Patient Portal"
echo "uv run python path_generate.py \\"
echo "  --project 'Patient Management System' \\"
echo "  --domain healthcare \\"
echo "  --requirements 'Patient records, appointment scheduling, telemedicine, billing integration' \\"
echo "  --constraints 'HIPAA compliance, 24/7 availability, secure data handling' \\"
echo "  --stakeholders 'Patients, Doctors, Nurses, Administrative Staff, Insurance Providers' \\"
echo "  --compliance 'HIPAA, HL7 FHIR, HITECH, state medical regulations'"
echo ""

echo "5️⃣  IoT Example - Smart Building System"
echo "uv run python path_generate.py \\"
echo "  --project 'Smart Building Management' \\"
echo "  --domain iot \\"
echo "  --requirements 'Sensor monitoring, energy management, security systems, predictive maintenance' \\"
echo "  --constraints 'Real-time processing, edge computing, battery-powered devices' \\"
echo "  --stakeholders 'Building Managers, Tenants, Maintenance Staff, Energy Providers' \\"
echo "  --compliance 'IoT security standards, energy regulations, building codes'"
echo ""

echo "6️⃣  Interactive Mode"
echo "uv run python path_generate.py --interactive"
echo ""

echo "7️⃣  Using Requirements File"
echo "uv run python path_generate.py --project 'My Project' --requirements-file templates/requirements_template.yaml"
echo ""

echo "8️⃣  Using UV Scripts"
echo "uv run generate-artifacts --project 'Quick Project' --domain business"
echo ""

echo "9️⃣  Using as Python Module"
echo "uv run python -m path_framework.phases.arch.generate_artifacts --project 'Module Project' --domain data"
echo ""

echo "🔟 After installation as package"
echo "path-generate --project 'Installed Project' --domain protocol"
echo ""

echo "📋 All generated artifacts will be in: projects/{PROJECT_NAME}/path_artifacts/"
echo ""
echo "✅ Ready to generate PATH Framework compliant architecture artifacts!"
