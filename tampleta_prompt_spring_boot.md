Crie um projeto Spring Boot 3.2 completo em Java 17 com Maven para um **Sistema [BOLETO_BANCARIO]**.

## Especificações Técnicas
- **Spring Boot**: 3.2.x
- **Java**: 17
- **Build Tool**: Maven
- **Packaging**: JAR
- **Arquitetura**: REST API com padrão MVC

## Dependências Base
```xml
- Spring Boot Starter Web
- Spring Boot Starter Data JPA
- Spring Boot Starter Validation
- Spring Boot Starter Security
- Spring Boot Starter Test
- Spring Boot DevTools
- Spring Boot Actuator
- H2 Database (desenvolvimento)
- MySQL Driver (produção)
- Lombok
- MapStruct
- Springdoc OpenAPI (Swagger)
- Apache Commons Lang3
- Jackson para JSON
```

## ⚠️ OBRIGATÓRIO: Estrutura Base de Entidades

**IMPORTANTE: Você DEVE gerar as entidades JPA completas com anotações. Não pule esta seção!**

### TEMPLATE - Entidade Principal (SEMPRE GERAR)
```java
@Entity
@Table(name = "entidade_principal")
@Data
@NoArgsConstructor
@AllArgsConstructor
public class EntidadePrincipal {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @Column(nullable = false)
    private String nome; // ou titulo
    
    private String descricao;
    
    @Enumerated(EnumType.STRING)
    private StatusEnum status;
    
    @Column(nullable = false)
    private Boolean ativo = true;
    
    @CreationTimestamp
    @Column(nullable = false, updatable = false)
    private LocalDateTime dataCriacao;
    
    @UpdateTimestamp
    private LocalDateTime dataAtualizacao;
}
```

### TEMPLATE - Entidade de Relacionamento (SE APLICÁVEL)
```java
@Entity
@Table(name = "entidade_relacionamento")
@Data
@NoArgsConstructor
@AllArgsConstructor
public class EntidadeRelacionamento {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @Column(nullable = false)
    private String nome;
    
    @Column(unique = true)
    private String codigo;
    
    @Enumerated(EnumType.STRING)
    private TipoEnum tipo;
    
    @Column(nullable = false)
    private Boolean ativo = true;
}
```

### TEMPLATE - Enums Base (SEMPRE GERAR)
```java
public enum StatusEnum {
    ATIVO("Ativo"),
    INATIVO("Inativo"),
    PENDENTE("Pendente"),
    CANCELADO("Cancelado");
    
    private final String descricao;
    
    StatusEnum(String descricao) {
        this.descricao = descricao;
    }
    
    public String getDescricao() {
        return descricao;
    }
}
```

**INSTRUÇÃO CRÍTICA PARA O LLM:**
- Sempre gere pelo menos 2-3 entidades JPA completas
- Use anotações Spring Data JPA apropriadas
- Inclua relacionamentos (@ManyToOne, @OneToMany, etc.)
- Gere os enums correspondentes


## Funcionalidades Padrão

### 1. CRUD Completo
- **POST /api/[recurso]** - Criar
- **GET /api/[recurso]** - Listar (paginado com filtros)
- **GET /api/[recurso]/{id}** - Buscar por ID
- **PUT /api/[recurso]/{id}** - Atualizar
- **DELETE /api/[recurso]/{id}** - Inativar/Excluir

### 2. Endpoints de Busca
- **GET /api/[recurso]/buscar** - Busca avançada
- **GET /api/[recurso]/ativos** - Listar apenas ativos
- **GET /api/[recurso]/por-status/{status}** - Filtrar por status

### 3. Relatórios Base
- **GET /api/relatorios/[recurso]** - Relatório geral
- **GET /api/relatorios/[recurso]/periodo** - Relatório por período
- **GET /api/relatorios/[recurso]/estatisticas** - Estatísticas

## Configurações Padrão

### application.yml
```yaml
spring:
  profiles:
    active: dev
  datasource:
    url: jdbc:h2:mem:testdb
    driver-class-name: org.h2.Driver
  jpa:
    hibernate:
      ddl-auto: create-drop
    show-sql: true

app:
  name: ${APP_NAME:[BOLETO_BANCARIO]}
  version: 1.0.0
  config:
    default-page-size: 20
    max-page-size: 100
```

## Recursos Técnicos Incluídos

### 2. Validações
- Bean Validation (JSR-303)
- Validações customizadas
- Sanitização de dados
- Tratamento de entrada

### 3. Tratamento de Exceções
- Handler global de exceções
- Exceções customizadas
- Retornos padronizados (RFC 7807)
- Logging de erros

### 4. Documentação
- Swagger/OpenAPI 3.0
- Exemplos de requests/responses
- Descrições detalhadas
- Modelos de dados documentados

### 5. Testes
- Testes unitários (JUnit 5)
- Testes de integração
- Testes de controller (MockMvc)
- Testes de repository (DataJpaTest)
- Coverage mínimo de 80%

### 6. Monitoramento
- Actuator endpoints
- Health checks customizados
- Métricas de negócio
- Logs estruturados (JSON)


## Estrutura de Pacotes
```
com.empresa.[dominio]
├── config/           # Configurações
├── controller/       # Controllers REST
├── service/          # Lógica de negócio
├── repository/       # Acesso a dados
├── dto/             # DTOs e requests/responses
├── entity/          # Entidades JPA
├── exception/       # Exceções customizadas
├── util/            # Utilitários
├── validator/       # Validadores customizados
├── mapper/          # Mappers (MapStruct)
└── Application.java # Classe principal
```

## Containerização
```dockerfile
# Dockerfile incluído
# docker-compose.yml com MySQL/Redis
# Scripts de deployment
```

---

## 🎯 REQUISITOS DE NEGÓCIO ESPECÍFICOS


### Exemplo de Uso:
```
### Domínio: Sistema de Boleto Bancário

#### Entidades Específicas:
1. **Cliente**: nome, cpfCnpj, email, telefone, endereco
2. **Boleto**: nossoNumero, valor, dataVencimento, status, codigoBarras
3. **Banco**: codigo, nome, agencia, conta, carteira

#### Regras de Negócio:
1. Gerar código de barras automaticamente
2. Calcular juros de 1% ao mês após vencimento
3. Aplicar multa de 2% após vencimento
4. Enviar boleto por email
5. Gerar PDF do boleto

#### Funcionalidades Específicas:
- Cancelamento de boletos
- Registro de pagamentos
- Relatório de inadimplência
- Reenvio de boletos por email
- Consulta por nosso número

#### Validações Específicas:
- CPF/CNPJ válido
- Data de vencimento futura
- Valor maior que zero
- Email válido
```

---

## 🚨 INSTRUÇÕES CRÍTICAS PARA GERAÇÃO DE CÓDIGO

**ATENÇÃO GPT-4: Você DEVE seguir estas instruções obrigatoriamente:**

### 1. SEMPRE GERAR CÓDIGO COMPLETO
- ✅ Gere entidades JPA completas com todas as anotações
- ✅ Gere controllers REST com todos os endpoints
- ✅ Gere services com implementação real
- ✅ Gere repositories com queries customizadas
- ✅ Gere DTOs com validações Bean Validation
- ❌ NÃO use comentários como "// implementar lógica aqui"
- ❌ NÃO deixe métodos vazios ou com TODO

### 2. ESTRUTURA OBRIGATÓRIA DE ARQUIVOS
Você DEVE gerar pelo menos estes arquivos:
```
1. Application.java (classe principal)
2. Pelo menos 2 entidades JPA completas
3. Pelo menos 2 controllers REST
4. Pelo menos 2 services implementados
5. Pelo menos 2 repositories
6. Pelo menos 4 DTOs (Request/Response)
7. GlobalExceptionHandler
8. SecurityConfig
9. SwaggerConfig
10. application.yml
```

### 3. EXEMPLOS DE CÓDIGO OBRIGATÓRIOS
- Controllers com @RestController, @RequestMapping, @Valid
- Services com @Service, @Transactional
- Repositories com @Repository, queries customizadas
- DTOs com @Valid, @NotNull, @Size, etc.
- Entidades com @Entity, @Table, relacionamentos JPA

### 4. VALIDAÇÃO DE QUALIDADE
Cada arquivo deve ter:
- Imports completos
- Javadoc nas classes principais
- Tratamento de exceções
- Logs estruturados
- Código funcional (sem placeholders)


## ⚠️ OBRIGATÓRIO: resumo geral

**IMPORTANTE: Ao final do processo liste todos os artefatos que geram gerado para conferência interna.