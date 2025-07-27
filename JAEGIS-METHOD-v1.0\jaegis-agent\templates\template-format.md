# {{Project Name}} - MD Template Format Guide
*Generated with JAEGIS Enhanced Validation & Research*

[[LLM: VALIDATION CHECKPOINT - Review shared context from template requirements and validate all format specifications. Integrate web research findings for current template design standards and documentation best practices.]]

## Executive Summary

[[LLM: RESEARCH INTEGRATION - Include current template design best practices and validated format methodologies. All template formats must be supported by current documentation standards and usability research.]]

## Enhanced MD Template Format:

[[LLM: VALIDATION CHECKPOINT - All template formats must be validated for consistency, usability, and current documentation standards. Include research-backed template design methodologies and format principles.]]

- {{placeholder}} = Simple text replacement placeholder with validation intelligence
- [[LLM: instruction]] = Enhanced instructions for the LLM with validation capabilities (not included in output)
- <<REPEAT: section_name>> ... <</REPEAT>> = Repeating section with research-backed methodologies
- ^^CONDITION: condition_name^^ ... ^^/CONDITION: condition_name^^ = Conditional section that will render if the condition_name logically applies with validation intelligence
- @{example: content} = Single line example content for LLM guidance with validation - do not render
- @{example} ... @{/example} = Multi-line example content for LLM guidance with research backing - do not render

## Critical Template Usage Rules

- CRITICAL: Never display or output template markup formatting, LLM instructions or examples
  - they MUST be used by you the agent only, AND NEVER shown to users in chat or documented output\*\*
- Present only the final, clean content to users
- Replace template variables with actual project-specific content
- Show examples only when they add value, without the markup
- Process all conditional logic internally - show only relevant sections
- For Canvas mode: Update the document with clean, formatted content only

@{example}

# My Template Foo

[[LLM: Check the current system date and if the user name is unknown, just say hello]]
Hello {{users name}}, this is your foo report for {{todays date}}

<<REPEAT: single_foo>>
[[LLM: For Each Foo, Create a matching creative Bar]]

## Foo: {{Bar}}

<</REPEAT>>

^^CONDITION: if_BAZ_exists^^

## BAZ

### You haz BAZ! Here is your daily Baz Forecast!

[[LLM: Give the user their daily baz report here]]
^^/CONDITION: if_BAZ_exists^^

@{/example}
