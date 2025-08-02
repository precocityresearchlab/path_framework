# Quick Start Example: Simple REST API

This example shows how to apply PATH framework to a simple REST API project.

## Project Overview
**Goal**: Build a task management REST API
**Technology**: Node.js + Express + PostgreSQL
**Timeline**: 4 weeks
**Team**: 3 developers + 1 DevOps engineer

## Phase 1: Architecture (Week 1)

### Requirements Analysis
```yaml
# requirements.yaml
product_goals:
  - "Provide task management API for mobile app"
  - "Support 1000 concurrent users"
  - "99% uptime SLA"

functional_requirements:
  - "CRUD operations for tasks"
  - "User authentication and authorization"
  - "Task filtering and search"

non_functional_requirements:
  - "Response time < 200ms"
  - "REST API compliance"
  - "PostgreSQL database"
```

### Architecture Design (Human + AI Agents)
```yaml
# system_architecture.yaml
architecture_pattern: "Clean Architecture"
technology_stack:
  runtime: "Node.js 18"
  framework: "Express.js"
  database: "PostgreSQL 14"
  orm: "Prisma"
  auth: "JWT"

layers:
  presentation: "REST API Controllers"
  application: "Use Cases / Services"
  domain: "Task Entity, Business Rules"
  infrastructure: "Database, External APIs"
```

### Component Design
```yaml
# component_designs.yaml
components:
  task_controller:
    responsibility: "HTTP request/response handling"
    dependencies: ["task_service", "auth_middleware"]
    
  task_service:
    responsibility: "Business logic orchestration"
    dependencies: ["task_repository", "validation_service"]
    
  task_repository:
    responsibility: "Data persistence abstraction"
    dependencies: ["database_connection"]
```

## Phase 2: TDD Implementation (Week 2-3)

### TDD Workflow (Human + AI Agents)

**Day 1: Domain Models**
```javascript
// tests/task.test.js - RED phase
describe('Task Entity', () => {
  it('should create valid task with required fields', () => {
    const task = new Task({
      title: 'Learn PATH framework',
      description: 'Study the methodology',
      userId: 'user123'
    });
    expect(task.isValid()).toBe(true);
  });
});

// src/domain/task.js - GREEN phase
class Task {
  constructor({ title, description, userId }) {
    this.title = title;
    this.description = description;
    this.userId = userId;
    this.status = 'pending';
    this.createdAt = new Date();
  }
  
  isValid() {
    return this.title && this.userId;
  }
}

// REFACTOR phase - Add validation, error handling
```

**Day 2-3: Service Layer**
```javascript
// tests/task-service.test.js
describe('TaskService', () => {
  it('should create task and persist to repository', async () => {
    const taskData = { title: 'Test', userId: 'user123' };
    const result = await taskService.createTask(taskData);
    expect(result.id).toBeDefined();
    expect(mockRepository.save).toHaveBeenCalled();
  });
});
```

**Day 4-5: API Layer**
```javascript
// tests/task-controller.test.js
describe('TaskController', () => {
  it('POST /tasks should create new task', async () => {
    const response = await request(app)
      .post('/tasks')
      .send({ title: 'Test task', description: 'Test' })
      .set('Authorization', 'Bearer validtoken');
    
    expect(response.status).toBe(201);
    expect(response.body.title).toBe('Test task');
  });
});
```

### Coverage Results
- Week 2 End: 85% coverage
- Week 3 End: 92% coverage
- Quality Gates: ✅ All passed

## Phase 3: DevOps (Week 4)

### CI/CD Pipeline
```yaml
# .github/workflows/ci-cd.yml
name: PATH Framework CI/CD
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with: { node-version: '18' }
      - run: npm ci
      - run: npm test
      - run: npm run test:coverage
      - name: Check coverage threshold
        run: |
          COVERAGE=$(npm run test:coverage:check | grep -o '[0-9]*%' | head -1 | tr -d '%')
          if [ $COVERAGE -lt 90 ]; then
            echo "Coverage $COVERAGE% below 90% threshold"
            exit 1
          fi

  deploy:
    needs: test
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to staging
        run: echo "Deploy to staging environment"
      - name: Run integration tests
        run: echo "Run integration test suite"
      - name: Deploy to production
        run: echo "Deploy to production environment"
```

### Infrastructure as Code
```yaml
# infrastructure/database.yml
apiVersion: v1
kind: ConfigMap
metadata:
  name: postgres-config
data:
  POSTGRES_DB: task_management
  POSTGRES_USER: taskuser

---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: task-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: task-api
  template:
    spec:
      containers:
      - name: task-api
        image: task-api:latest
        ports:
        - containerPort: 3000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: db-secret
              key: connection-string
```

### Monitoring Setup
```yaml
# monitoring/alerts.yml
alerts:
  - name: "High Response Time"
    condition: "avg_response_time > 200ms"
    severity: "warning"
    
  - name: "Low Success Rate"
    condition: "success_rate < 95%"
    severity: "critical"
    
  - name: "High Error Rate"
    condition: "error_rate > 5%"
    severity: "critical"
```

## Phase 4: Operations (Ongoing)

### Daily Operations Checklist
- [ ] Check system health dashboard
- [ ] Review overnight alerts and incidents
- [ ] Monitor performance metrics
- [ ] Validate backup completion
- [ ] Security scan results review

### Key Metrics Tracking
```yaml
# operational_metrics.yaml
sla_targets:
  uptime: "99.9%"
  response_time: "< 200ms"
  error_rate: "< 1%"

current_performance:
  uptime: "99.95%"
  avg_response_time: "150ms"
  error_rate: "0.2%"
  
alerts_last_24h:
  total: 2
  resolved: 2
  critical: 0
```

## Results Summary

### Technical Achievements
- ✅ API deployed and operational
- ✅ 92% test coverage maintained
- ✅ <200ms average response time
- ✅ 99.95% uptime achieved

### Process Benefits
- ✅ Systematic development approach
- ✅ Human-AI collaboration effective
- ✅ Quality gates prevented issues
- ✅ Comprehensive documentation

### Lessons Learned
1. **Human-AI Balance**: Initial agent recommendations needed human refinement
2. **TDD Discipline**: Strict TDD cycles improved code quality significantly
3. **Quality Gates**: Coverage thresholds caught potential issues early
4. **Integration**: Cross-phase handoffs worked smoothly with YAML artifacts

### Time Investment
- **Architecture**: 8 hours (vs typical 4) - but prevented 3 days of rework
- **TDD**: 2 weeks (vs typical 1.5) - but reduced bug fixing by 70%
- **DevOps**: 3 days (vs typical 1) - but deployment issues reduced to zero
- **Overall**: 10% more upfront time, 50% less bug fixing and rework

## Next Steps
1. **Scale Pattern**: Apply to larger microservice
2. **Team Training**: Train additional teams on PATH methodology
3. **Process Refinement**: Customize for organization-specific needs
4. **Tool Integration**: Implement organization-preferred tools

---

**Project Success**: ✅ Delivered on time with high quality
**Framework Effectiveness**: 9/10 - Significant improvement over traditional approach
**Team Satisfaction**: 8/10 - Learning curve but valuable methodology
