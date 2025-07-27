#!/bin/bash

# N.L.D.S. Development Environment Setup Script
# JAEGIS Enhanced Agent System v2.2 - Tier 0 Component

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Main setup function
main() {
    log_info "Starting N.L.D.S. Development Environment Setup..."
    
    # Check prerequisites
    check_prerequisites
    
    # Setup Python environment
    setup_python_environment
    
    # Setup Docker environment
    setup_docker_environment
    
    # Setup database
    setup_database
    
    # Setup monitoring
    setup_monitoring
    
    # Setup pre-commit hooks
    setup_pre_commit_hooks
    
    # Run initial tests
    run_initial_tests
    
    log_success "N.L.D.S. Development Environment Setup Complete!"
    print_next_steps
}

# Check prerequisites
check_prerequisites() {
    log_info "Checking prerequisites..."
    
    # Check Python
    if ! command_exists python3; then
        log_error "Python 3 is not installed. Please install Python 3.9 or higher."
        exit 1
    fi
    
    python_version=$(python3 --version | cut -d' ' -f2)
    log_info "Python version: $python_version"
    
    # Check pip
    if ! command_exists pip3; then
        log_error "pip3 is not installed. Please install pip."
        exit 1
    fi
    
    # Check Docker
    if ! command_exists docker; then
        log_error "Docker is not installed. Please install Docker."
        exit 1
    fi
    
    # Check Docker Compose
    if ! command_exists docker-compose; then
        log_error "Docker Compose is not installed. Please install Docker Compose."
        exit 1
    fi
    
    # Check Git
    if ! command_exists git; then
        log_error "Git is not installed. Please install Git."
        exit 1
    fi
    
    log_success "All prerequisites are installed."
}

# Setup Python environment
setup_python_environment() {
    log_info "Setting up Python environment..."
    
    # Create virtual environment if it doesn't exist
    if [ ! -d "venv" ]; then
        log_info "Creating virtual environment..."
        python3 -m venv venv
    fi
    
    # Activate virtual environment
    log_info "Activating virtual environment..."
    source venv/bin/activate
    
    # Upgrade pip
    log_info "Upgrading pip..."
    pip install --upgrade pip
    
    # Install dependencies
    log_info "Installing Python dependencies..."
    pip install -r requirements.txt
    pip install -r requirements-dev.txt
    
    # Download spaCy models
    log_info "Downloading spaCy models..."
    python -m spacy download en_core_web_lg
    python -m spacy download xx_ent_wiki_sm
    
    # Download NLTK data
    log_info "Downloading NLTK data..."
    python -c "
import nltk
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('vader_lexicon')
nltk.download('averaged_perceptron_tagger')
"
    
    log_success "Python environment setup complete."
}

# Setup Docker environment
setup_docker_environment() {
    log_info "Setting up Docker environment..."
    
    # Create necessary directories
    mkdir -p data logs models
    mkdir -p database redis nginx monitoring
    
    # Create environment file if it doesn't exist
    if [ ! -f ".env" ]; then
        log_info "Creating .env file..."
        cat > .env << EOF
# N.L.D.S. Development Environment Variables
ENVIRONMENT=development
LOG_LEVEL=DEBUG
SECRET_KEY=dev_secret_key_change_in_production
DATABASE_URL=postgresql://nlds_user:nlds_password@localhost:5432/nlds_dev
REDIS_URL=redis://localhost:6379/0
JAEGIS_ENDPOINT=http://localhost:8001
AMASIAP_ENDPOINT=http://localhost:8002
EOF
    fi
    
    # Build Docker images
    log_info "Building Docker images..."
    docker-compose -f docker-compose.dev.yml build
    
    log_success "Docker environment setup complete."
}

# Setup database
setup_database() {
    log_info "Setting up database..."
    
    # Start database services
    log_info "Starting database services..."
    docker-compose -f docker-compose.dev.yml up -d postgres redis
    
    # Wait for services to be ready
    log_info "Waiting for services to be ready..."
    sleep 10
    
    # Run database migrations
    log_info "Running database migrations..."
    # Add migration commands here when available
    
    log_success "Database setup complete."
}

# Setup monitoring
setup_monitoring() {
    log_info "Setting up monitoring..."
    
    # Create monitoring configuration
    mkdir -p monitoring/prometheus monitoring/grafana/dashboards monitoring/grafana/datasources
    
    # Create Prometheus configuration
    cat > monitoring/prometheus.yml << EOF
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: 'nlds-api'
    static_configs:
      - targets: ['nlds-api:8000']
    metrics_path: '/metrics'
    scrape_interval: 5s
EOF
    
    # Create Grafana datasource configuration
    cat > monitoring/grafana/datasources/prometheus.yml << EOF
apiVersion: 1

datasources:
  - name: Prometheus
    type: prometheus
    access: proxy
    url: http://prometheus:9090
    isDefault: true
EOF
    
    log_success "Monitoring setup complete."
}

# Setup pre-commit hooks
setup_pre_commit_hooks() {
    log_info "Setting up pre-commit hooks..."
    
    # Create pre-commit configuration
    cat > .pre-commit-config.yaml << EOF
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.4.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
      - id: check-merge-conflict
  
  - repo: https://github.com/psf/black
    rev: 23.11.0
    hooks:
      - id: black
        language_version: python3
  
  - repo: https://github.com/pycqa/isort
    rev: 5.12.0
    hooks:
      - id: isort
  
  - repo: https://github.com/pycqa/flake8
    rev: 6.1.0
    hooks:
      - id: flake8
  
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.7.1
    hooks:
      - id: mypy
        additional_dependencies: [types-all]
EOF
    
    # Install pre-commit hooks
    if command_exists pre-commit; then
        log_info "Installing pre-commit hooks..."
        pre-commit install
    else
        log_warning "pre-commit not found. Install it with: pip install pre-commit"
    fi
    
    log_success "Pre-commit hooks setup complete."
}

# Run initial tests
run_initial_tests() {
    log_info "Running initial tests..."
    
    # Start all services
    log_info "Starting all services..."
    docker-compose -f docker-compose.dev.yml up -d
    
    # Wait for services to be ready
    log_info "Waiting for services to be ready..."
    sleep 30
    
    # Run health checks
    log_info "Running health checks..."
    
    # Check API health
    if curl -f http://localhost:8000/health > /dev/null 2>&1; then
        log_success "N.L.D.S. API is healthy"
    else
        log_warning "N.L.D.S. API health check failed"
    fi
    
    # Check database connection
    if docker-compose -f docker-compose.dev.yml exec -T postgres pg_isready -U nlds_user -d nlds_dev > /dev/null 2>&1; then
        log_success "Database is ready"
    else
        log_warning "Database connection failed"
    fi
    
    # Check Redis connection
    if docker-compose -f docker-compose.dev.yml exec -T redis redis-cli ping > /dev/null 2>&1; then
        log_success "Redis is ready"
    else
        log_warning "Redis connection failed"
    fi
    
    # Run unit tests
    log_info "Running unit tests..."
    if pytest tests/unit/ -v --tb=short; then
        log_success "Unit tests passed"
    else
        log_warning "Some unit tests failed"
    fi
    
    log_success "Initial tests complete."
}

# Print next steps
print_next_steps() {
    echo ""
    log_info "Next steps:"
    echo "1. Activate the virtual environment: source venv/bin/activate"
    echo "2. Start the development environment: docker-compose -f docker-compose.dev.yml up"
    echo "3. Access the API documentation: http://localhost:8000/docs"
    echo "4. Access Grafana dashboard: http://localhost:3000 (admin/admin)"
    echo "5. Access Prometheus: http://localhost:9090"
    echo "6. Access Kibana: http://localhost:5601"
    echo ""
    log_info "Development environment is ready!"
}

# Run main function
main "$@"
