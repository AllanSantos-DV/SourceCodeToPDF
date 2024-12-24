# Guia de Contribuição

Obrigado por considerar contribuir para o **Conversor de Código-Fonte para PDF**! Este guia ajudará você a entender como colaborar de forma eficiente.

---

## Como Contribuir

### 1. Reportar Problemas
- Acesse a página de *Issues* no repositório.
- Verifique se o problema que deseja relatar já foi registrado.
- Caso não tenha sido, abra uma nova *Issue* incluindo:
  - Uma descrição clara do problema.
  - Passos para reproduzi-lo.
  - Logs ou capturas de tela, se possível.

### 2. Sugerir Melhorias
- Abra uma *Issue* com a tag **enhancement** explicando:
  - A funcionalidade desejada.
  - Benefícios para o projeto.

### 3. Submeter Mudanças
1. **Faça um Fork do Repositório**
   - Crie um fork do projeto em sua conta.
   - Clone o repositório forkado para sua máquina local:
     ```bash
     git clone https://github.com/seu-usuario/conversor-pdf.git
     cd conversor-pdf
     ```

2. **Crie uma Nova Branch**
   - Baseie sua branch na branch principal:
     ```bash
     git checkout -b minha-contribuicao
     ```

3. **Implemente e Teste Suas Mudanças**
   - Certifique-se de seguir as diretrizes de código descritas abaixo.
   - Execute testes para garantir que tudo funciona:
     ```bash
     pytest
     ```

4. **Envie Suas Mudanças**
   - Faça commit das alterações:
     ```bash
     git add .
     git commit -m "Descrição clara da mudança"
     ```
   - Envie para seu repositório forkado:
     ```bash
     git push origin minha-contribuicao
     ```

5. **Abra um Pull Request (PR)**
   - No repositório original, clique em **New Pull Request**.
   - Explique suas mudanças no PR e inclua links para a *Issue* relacionada, se houver.

---

## Padrões de Código

### Estilo de Código
- Siga as diretrizes da [PEP 8](https://peps.python.org/pep-0008/).
- Use nomes de variáveis claros e descritivos.
- Adicione docstrings a todas as classes, métodos e funções.

### Formatação
- Utilize o `black` para garantir formatação consistente:
  ```bash
  black .
  ```

### Testes
- Adicione ou atualize testes relacionados às suas alterações.
- Certifique-se de que todos os testes passam antes de enviar seu PR:
  ```bash
  pytest
  ```

---

## Checklist para Envio de PR
Antes de enviar seu Pull Request:
- [ ] A branch está atualizada com a branch principal.
- [ ] Todas as alterações foram testadas e estão funcionando.
- [ ] O código segue as diretrizes de estilo e qualidade.
- [ ] Testes foram adicionados ou atualizados para cobrir as mudanças.

---

## Recursos Adicionais

- [Documentação Oficial do GitHub sobre Pull Requests](https://docs.github.com/en/pull-requests)
- [PEP 8: Estilo de Código Python](https://peps.python.org/pep-0008/)

Agradecemos sua colaboração! :tada:

