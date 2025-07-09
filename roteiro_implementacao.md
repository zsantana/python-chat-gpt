# Prompt para Geração de Aplicação Spring Boot com DDD

Você é um especialista em desenvolvimento Java com Spring Boot, Domain-Driven Design (DDD) e princípios SOLID. Sua tarefa é gerar uma aplicação completa seguindo as especificações abaixo.

## Contexto do Domínio
**[IMPORTANTE: O usuário deve especificar o domínio específico aqui - ex: "Sistema de Gestão de Boletos Bancários"]**

## Estrutura do Projeto
- **Tipo**: Projeto Maven multi-módulo
- **Módulos**: `domain`, `application`, `infrastructure`, `presentation`
- **Organização**: Por bounded context (ex: boleto, cliente, pagamento)
- **Perfis**: dev, prod
- **Build Tool**: Maven

## Dependências Obrigatórias
```xml
- Spring Boot Starter Web
- Spring Boot Starter Data JPA
- Spring Boot Starter Security
- Spring Boot Starter Validation
- H2 Database (perfil dev)
- Bean Validation
- Spring Boot Starter Test
```

## Arquitetura e Camadas

### 1. Domain Layer (Módulo domain)
- **Entidades**: Implementar com identidade única, invariantes e comportamentos
- **Value Objects**: Objetos imutáveis sem identidade
- **Aggregates**: Raízes de agregado com consistência transacional
- **Domain Services**: Lógica de negócio que não pertence a uma entidade específica
- **Repositories (interfaces)**: Contratos para persistência
- **Domain Events**: Para comunicação entre agregados (opcional)
- **Specifications**: Para encapsular regras de negócio complexas

### 2. Application Layer (Módulo application)
- **Use Cases/Services**: Orquestração de operações de negócio
- **DTOs**: Para transferência de dados entre camadas
- **Mappers**: Conversão entre DTOs e entidades de domínio
- **Application Services**: Coordenação de fluxos de trabalho
- **Command/Query Handlers**: Separação de responsabilidades CQRS (opcional)

### 3. Infrastructure Layer (Módulo infrastructure)
- **Repository Implementations**: Implementações concretas usando Spring Data JPA
- **JPA Entities**: Mapeamento para persistência
- **Configuration Classes**: Configurações do Spring
- **External Services**: Integrações com APIs externas
- **Event Publishers**: Implementação de eventos de domínio

### 4. Presentation Layer (Módulo presentation)
- **REST Controllers**: Endpoints HTTP seguindo padrões REST
- **Request/Response DTOs**: Contratos de API
- **Exception Handlers**: Tratamento global de exceções
- **Validation**: Validação de entrada usando Bean Validation
- **Security Configuration**: Configuração de segurança

## Padrões e Princípios a Seguir

### Domain-Driven Design
- ✅ Bounded Context bem definido
- ✅ Ubiquitous Language consistente
- ✅ Rich Domain Model (entidades com comportamento)
- ✅ Aggregates com invariantes
- ✅ Repository pattern
- ✅ Domain Events para desacoplamento

### Princípios SOLID
- ✅ **SRP**: Cada classe com uma única responsabilidade
- ✅ **OCP**: Aberto para extensão, fechado para modificação
- ✅ **LSP**: Substituição de Liskov respeitada
- ✅ **ISP**: Interfaces segregadas e específicas
- ✅ **DIP**: Dependência de abstrações, não de concretizações

### Design Patterns
- **Repository**: Para abstração de persistência
- **Factory**: Para criação de objetos complexos
- **Builder**: Para construção de objetos com muitos parâmetros
- **Strategy**: Para algoritmos intercambiáveis
- **Observer**: Para eventos de domínio

## Configurações Técnicas

### Banco de Dados
```yaml
# application-dev.yml
spring:
  datasource:
    url: jdbc:h2:mem:testdb
    driver-class-name: org.h2.Driver
  h2:
    console:
      enabled: true
  jpa:
    hibernate:
      ddl-auto: create-drop
    show-sql: true
```

### Segurança
- Configuração básica do Spring Security
- Autenticação HTTP Basic para desenvolvimento
- Proteção de endpoints REST

### Validação
- Bean Validation nas DTOs de entrada
- Validação de domínio nas entidades
- Tratamento de erros de validação

### Logging
```yaml
logging:
  level:
    com.empresa.projeto: INFO
    org.springframework: INFO
    org.hibernate: WARN
```

## Estrutura de Resposta HTTP

### Sucesso
```json
{
  "status": "success",
  "data": { /* objeto retornado */ },
  "timestamp": "2024-01-01T10:00:00Z"
}
```

### Erro de Validação
```json
{
  "status": "error",
  "message": "Validation failed",
  "errors": [
    {
      "field": "campo",
      "message": "mensagem de erro"
    }
  ],
  "timestamp": "2024-01-01T10:00:00Z"
}
```

## Testes Obrigatórios

### Unit Tests
- Testes de domínio (entidades, value objects, domain services)
- Testes de application services
- Testes de controllers (usando MockMvc)

### Integration Tests
- Testes de repositório com @DataJpaTest
- Testes de API completos com @SpringBootTest

## Deliverables Esperados

1. **Estrutura completa do projeto** com todos os módulos
2. **pom.xml** principal e dos módulos
3. **Configurações** (application.yml para dev/prod)
4. **Código fonte** de todas as camadas
5. **Testes unitários** e de integração
6. **README.md** com instruções de uso
7. **Dockerfile** para containerização (opcional)

## Instruções Específicas

1. **Nomeação**: Use nomes em português para classes de domínio, inglês para infraestrutura
2. **Documentação**: Javadoc nas classes públicas e métodos complexos
3. **Tratamento de Exceções**: Exceções específicas de domínio e tratamento global
4. **Validação**: Validação rigorosa em todas as entradas
5. **Logging**: Logs estruturados para auditoria e monitoramento
6. **Clean Code**: Código limpo, legível e bem estruturado

## Exemplo de Endpoint
```java
@PostMapping("/api/boletos")
public ResponseEntity<BoletoResponse> criarBoleto(@Valid @RequestBody CriarBoletoRequest request) {
    // Implementação seguindo os padrões especificados
}
```

---

**Importante**: Gere código funcional, testável e pronto para produção, seguindo todas as especificações acima. O código deve ser profissional e aderente às melhores práticas de desenvolvimento Java/Spring Boot.