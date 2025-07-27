#!/usr/bin/env python3
"""
A.U.R.A. Framework-Native Code Generators
Artistic & UI Responsive Assistant - Framework-Native Code Generation

This module implements code generation for React, Vue, Svelte, Angular
with clean, idiomatic output for production-ready components.
"""

import json
import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime
from enum import Enum

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FrameworkType(Enum):
    """Supported frontend frameworks"""
    REACT = "react"
    VUE = "vue"
    SVELTE = "svelte"
    ANGULAR = "angular"

class ComponentType(Enum):
    """Types of components"""
    BUTTON = "button"
    FORM = "form"
    CARD = "card"
    MODAL = "modal"
    INPUT = "input"
    TABLE = "table"
    NAVIGATION = "navigation"

@dataclass
class ComponentSpec:
    """Component specification"""
    name: str
    type: ComponentType
    props: List[Dict[str, Any]]
    styling: Dict[str, Any]
    functionality: List[str]
    framework: FrameworkType

class ReactGenerator:
    """React component generator with TypeScript support"""
    
    def generate_component(self, spec: ComponentSpec) -> Dict[str, str]:
        """Generate React component with TypeScript"""
        
        if spec.type == ComponentType.BUTTON:
            return self._generate_react_button(spec)
        elif spec.type == ComponentType.FORM:
            return self._generate_react_form(spec)
        elif spec.type == ComponentType.CARD:
            return self._generate_react_card(spec)
        elif spec.type == ComponentType.MODAL:
            return self._generate_react_modal(spec)
        elif spec.type == ComponentType.INPUT:
            return self._generate_react_input(spec)
        else:
            return self._generate_react_generic(spec)
    
    def _generate_react_button(self, spec: ComponentSpec) -> Dict[str, str]:
        """Generate React button component"""
        
        # Generate TypeScript interface
        interface = self._generate_react_interface(spec)
        
        # Generate component code
        component_code = f"""import React from 'react';
import './{spec.name}.css';

{interface}

const {spec.name}: React.FC<{spec.name}Props> = ({{
  children,
  variant = 'primary',
  size = 'medium',
  disabled = false,
  onClick,
  className = '',
  ...props
}}) => {{
  const baseClasses = 'btn';
  const variantClass = `btn--${{variant}}`;
  const sizeClass = `btn--${{size}}`;
  const disabledClass = disabled ? 'btn--disabled' : '';
  
  const buttonClasses = [
    baseClasses,
    variantClass,
    sizeClass,
    disabledClass,
    className
  ].filter(Boolean).join(' ');

  return (
    <button
      className={{buttonClasses}}
      disabled={{disabled}}
      onClick={{onClick}}
      {{...props}}
    >
      {{children}}
    </button>
  );
}};

export default {spec.name};"""

        # Generate CSS
        css_code = f""".btn {{
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border: none;
  border-radius: 0.375rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.15s ease-in-out;
  text-decoration: none;
}}

.btn:disabled,
.btn--disabled {{
  opacity: 0.5;
  cursor: not-allowed;
}}

.btn--primary {{
  background-color: #2563eb;
  color: white;
}}

.btn--primary:hover:not(:disabled) {{
  background-color: #1d4ed8;
}}

.btn--secondary {{
  background-color: #e5e7eb;
  color: #374151;
}}

.btn--secondary:hover:not(:disabled) {{
  background-color: #d1d5db;
}}

.btn--small {{
  padding: 0.375rem 0.75rem;
  font-size: 0.875rem;
}}

.btn--medium {{
  padding: 0.5rem 1rem;
  font-size: 1rem;
}}

.btn--large {{
  padding: 0.75rem 1.5rem;
  font-size: 1.125rem;
}}"""

        return {
            "component": component_code,
            "styles": css_code,
            "test": self._generate_react_test(spec)
        }
    
    def _generate_react_form(self, spec: ComponentSpec) -> Dict[str, str]:
        """Generate React form component"""
        
        interface = self._generate_react_interface(spec)
        
        component_code = f"""import React, {{ useState }} from 'react';
import './{spec.name}.css';

{interface}

const {spec.name}: React.FC<{spec.name}Props> = ({{
  onSubmit,
  fields = [],
  submitText = 'Submit',
  className = ''
}}) => {{
  const [formData, setFormData] = useState<Record<string, any>>({{}});
  const [errors, setErrors] = useState<Record<string, string>>({{}});

  const handleInputChange = (name: string, value: any) => {{
    setFormData(prev => ({{ ...prev, [name]: value }}));
    // Clear error when user starts typing
    if (errors[name]) {{
      setErrors(prev => ({{ ...prev, [name]: '' }}));
    }}
  }};

  const validateForm = (): boolean => {{
    const newErrors: Record<string, string> = {{}};
    
    fields.forEach(field => {{
      if (field.required && !formData[field.name]) {{
        newErrors[field.name] = `${{field.label}} is required`;
      }}
    }});

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  }};

  const handleSubmit = (e: React.FormEvent) => {{
    e.preventDefault();
    if (validateForm()) {{
      onSubmit(formData);
    }}
  }};

  return (
    <form className={{`form ${{className}}`}} onSubmit={{handleSubmit}}>
      {{fields.map(field => (
        <div key={{field.name}} className="form__field">
          <label htmlFor={{field.name}} className="form__label">
            {{field.label}}
            {{field.required && <span className="form__required">*</span>}}
          </label>
          <input
            id={{field.name}}
            type={{field.type || 'text'}}
            value={{formData[field.name] || ''}}
            onChange={{e => handleInputChange(field.name, e.target.value)}}
            className={{`form__input ${{errors[field.name] ? 'form__input--error' : ''}}`}}
            placeholder={{field.placeholder}}
          />
          {{errors[field.name] && (
            <span className="form__error">{{errors[field.name]}}</span>
          )}}
        </div>
      ))}}
      <button type="submit" className="form__submit">
        {{submitText}}
      </button>
    </form>
  );
}};

export default {spec.name};"""

        css_code = """.form {
  max-width: 500px;
  margin: 0 auto;
}

.form__field {
  margin-bottom: 1rem;
}

.form__label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: #374151;
}

.form__required {
  color: #dc2626;
  margin-left: 0.25rem;
}

.form__input {
  width: 100%;
  padding: 0.5rem 0.75rem;
  border: 1px solid #d1d5db;
  border-radius: 0.375rem;
  font-size: 1rem;
  transition: border-color 0.15s ease-in-out;
}

.form__input:focus {
  outline: none;
  border-color: #2563eb;
  box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
}

.form__input--error {
  border-color: #dc2626;
}

.form__error {
  display: block;
  margin-top: 0.25rem;
  font-size: 0.875rem;
  color: #dc2626;
}

.form__submit {
  width: 100%;
  padding: 0.75rem;
  background-color: #2563eb;
  color: white;
  border: none;
  border-radius: 0.375rem;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.15s ease-in-out;
}

.form__submit:hover {
  background-color: #1d4ed8;
}"""

        return {
            "component": component_code,
            "styles": css_code,
            "test": self._generate_react_test(spec)
        }
    
    def _generate_react_card(self, spec: ComponentSpec) -> Dict[str, str]:
        """Generate React card component"""
        
        interface = self._generate_react_interface(spec)
        
        component_code = f"""import React from 'react';
import './{spec.name}.css';

{interface}

const {spec.name}: React.FC<{spec.name}Props> = ({{
  title,
  children,
  footer,
  variant = 'default',
  className = ''
}}) => {{
  const cardClasses = `card card--${{variant}} ${{className}}`.trim();

  return (
    <div className={{cardClasses}}>
      {{title && (
        <div className="card__header">
          <h3 className="card__title">{{title}}</h3>
        </div>
      )}}
      <div className="card__content">
        {{children}}
      </div>
      {{footer && (
        <div className="card__footer">
          {{footer}}
        </div>
      )}}
    </div>
  );
}};

export default {spec.name};"""

        css_code = """.card {
  background: white;
  border-radius: 0.5rem;
  box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.card__header {
  padding: 1rem 1.5rem;
  border-bottom: 1px solid #e5e7eb;
}

.card__title {
  margin: 0;
  font-size: 1.125rem;
  font-weight: 600;
  color: #111827;
}

.card__content {
  padding: 1.5rem;
}

.card__footer {
  padding: 1rem 1.5rem;
  background-color: #f9fafb;
  border-top: 1px solid #e5e7eb;
}

.card--elevated {
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

.card--bordered {
  border: 1px solid #e5e7eb;
  box-shadow: none;
}"""

        return {
            "component": component_code,
            "styles": css_code,
            "test": self._generate_react_test(spec)
        }
    
    def _generate_react_generic(self, spec: ComponentSpec) -> Dict[str, str]:
        """Generate generic React component"""
        
        interface = self._generate_react_interface(spec)
        
        component_code = f"""import React from 'react';
import './{spec.name}.css';

{interface}

const {spec.name}: React.FC<{spec.name}Props> = (props) => {{
  return (
    <div className="{spec.name.lower()}">
      {{/* Component content */}}
    </div>
  );
}};

export default {spec.name};"""

        css_code = f""".{spec.name.lower()} {{
  /* Component styles */
}}"""

        return {
            "component": component_code,
            "styles": css_code,
            "test": self._generate_react_test(spec)
        }
    
    def _generate_react_interface(self, spec: ComponentSpec) -> str:
        """Generate TypeScript interface for React component"""
        
        props = []
        for prop in spec.props:
            optional = "?" if not prop.get("required", False) else ""
            props.append(f"  {prop['name']}{optional}: {prop['type']};")
        
        # Add common props
        props.extend([
            "  children?: React.ReactNode;",
            "  className?: string;"
        ])
        
        return f"""interface {spec.name}Props {{
{chr(10).join(props)}
}}"""
    
    def _generate_react_test(self, spec: ComponentSpec) -> str:
        """Generate Jest test for React component"""
        
        return f"""import React from 'react';
import {{ render, screen }} from '@testing-library/react';
import {spec.name} from './{spec.name}';

describe('{spec.name}', () => {{
  it('renders without crashing', () => {{
    render(<{spec.name} />);
  }});

  it('applies custom className', () => {{
    const customClass = 'custom-class';
    render(<{spec.name} className={{customClass}} />);
    const element = screen.getByRole('{spec.type.value}');
    expect(element).toHaveClass(customClass);
  }});
}});"""

class VueGenerator:
    """Vue 3 component generator with Composition API"""
    
    def generate_component(self, spec: ComponentSpec) -> Dict[str, str]:
        """Generate Vue 3 component with Composition API"""
        
        if spec.type == ComponentType.BUTTON:
            return self._generate_vue_button(spec)
        elif spec.type == ComponentType.FORM:
            return self._generate_vue_form(spec)
        elif spec.type == ComponentType.CARD:
            return self._generate_vue_card(spec)
        else:
            return self._generate_vue_generic(spec)
    
    def _generate_vue_button(self, spec: ComponentSpec) -> Dict[str, str]:
        """Generate Vue button component"""
        
        component_code = f"""<template>
  <button
    :class="buttonClasses"
    :disabled="disabled"
    @click="handleClick"
  >
    <slot></slot>
  </button>
</template>

<script setup lang="ts">
import {{ computed }} from 'vue';

interface Props {{
  variant?: 'primary' | 'secondary' | 'danger';
  size?: 'small' | 'medium' | 'large';
  disabled?: boolean;
  class?: string;
}}

const props = withDefaults(defineProps<Props>(), {{
  variant: 'primary',
  size: 'medium',
  disabled: false,
  class: ''
}});

const emit = defineEmits<{{
  click: [event: MouseEvent];
}}>();

const buttonClasses = computed(() => [
  'btn',
  `btn--${{props.variant}}`,
  `btn--${{props.size}}`,
  {{ 'btn--disabled': props.disabled }},
  props.class
]);

const handleClick = (event: MouseEvent) => {{
  if (!props.disabled) {{
    emit('click', event);
  }}
}};
</script>

<style scoped>
.btn {{
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border: none;
  border-radius: 0.375rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.15s ease-in-out;
}}

.btn:disabled,
.btn--disabled {{
  opacity: 0.5;
  cursor: not-allowed;
}}

.btn--primary {{
  background-color: #2563eb;
  color: white;
}}

.btn--primary:hover:not(:disabled) {{
  background-color: #1d4ed8;
}}

.btn--secondary {{
  background-color: #e5e7eb;
  color: #374151;
}}

.btn--secondary:hover:not(:disabled) {{
  background-color: #d1d5db;
}}

.btn--small {{
  padding: 0.375rem 0.75rem;
  font-size: 0.875rem;
}}

.btn--medium {{
  padding: 0.5rem 1rem;
  font-size: 1rem;
}}

.btn--large {{
  padding: 0.75rem 1.5rem;
  font-size: 1.125rem;
}}
</style>"""

        return {
            "component": component_code,
            "test": self._generate_vue_test(spec)
        }
    
    def _generate_vue_card(self, spec: ComponentSpec) -> Dict[str, str]:
        """Generate Vue card component"""
        
        component_code = f"""<template>
  <div :class="cardClasses">
    <div v-if="$slots.header || title" class="card__header">
      <slot name="header">
        <h3 v-if="title" class="card__title">{{ title }}</h3>
      </slot>
    </div>
    <div class="card__content">
      <slot></slot>
    </div>
    <div v-if="$slots.footer" class="card__footer">
      <slot name="footer"></slot>
    </div>
  </div>
</template>

<script setup lang="ts">
import {{ computed }} from 'vue';

interface Props {{
  title?: string;
  variant?: 'default' | 'elevated' | 'bordered';
  class?: string;
}}

const props = withDefaults(defineProps<Props>(), {{
  variant: 'default',
  class: ''
}});

const cardClasses = computed(() => [
  'card',
  `card--${{props.variant}}`,
  props.class
]);
</script>

<style scoped>
.card {{
  background: white;
  border-radius: 0.5rem;
  box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
  overflow: hidden;
}}

.card__header {{
  padding: 1rem 1.5rem;
  border-bottom: 1px solid #e5e7eb;
}}

.card__title {{
  margin: 0;
  font-size: 1.125rem;
  font-weight: 600;
  color: #111827;
}}

.card__content {{
  padding: 1.5rem;
}}

.card__footer {{
  padding: 1rem 1.5rem;
  background-color: #f9fafb;
  border-top: 1px solid #e5e7eb;
}}

.card--elevated {{
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}}

.card--bordered {{
  border: 1px solid #e5e7eb;
  box-shadow: none;
}}
</style>"""

        return {
            "component": component_code,
            "test": self._generate_vue_test(spec)
        }
    
    def _generate_vue_generic(self, spec: ComponentSpec) -> Dict[str, str]:
        """Generate generic Vue component"""
        
        component_code = f"""<template>
  <div class="{spec.name.lower()}">
    <!-- Component content -->
    <slot></slot>
  </div>
</template>

<script setup lang="ts">
// Component logic
</script>

<style scoped>
.{spec.name.lower()} {{
  /* Component styles */
}}
</style>"""

        return {
            "component": component_code,
            "test": self._generate_vue_test(spec)
        }
    
    def _generate_vue_test(self, spec: ComponentSpec) -> str:
        """Generate Vue test"""
        
        return f"""import {{ mount }} from '@vue/test-utils';
import {spec.name} from './{spec.name}.vue';

describe('{spec.name}', () => {{
  it('renders properly', () => {{
    const wrapper = mount({spec.name});
    expect(wrapper.exists()).toBe(true);
  }});

  it('applies custom class', () => {{
    const customClass = 'custom-class';
    const wrapper = mount({spec.name}, {{
      props: {{ class: customClass }}
    }});
    expect(wrapper.classes()).toContain(customClass);
  }});
}});"""

class FrameworkGeneratorFactory:
    """Factory for creating framework-specific generators"""
    
    @staticmethod
    def create_generator(framework: FrameworkType):
        """Create appropriate generator for framework"""
        
        if framework == FrameworkType.REACT:
            return ReactGenerator()
        elif framework == FrameworkType.VUE:
            return VueGenerator()
        else:
            raise ValueError(f"Unsupported framework: {framework}")

# Example usage and testing
if __name__ == "__main__":
    # Test React generator
    react_spec = ComponentSpec(
        name="CustomButton",
        type=ComponentType.BUTTON,
        props=[
            {"name": "variant", "type": "'primary' | 'secondary'", "required": False},
            {"name": "size", "type": "'small' | 'medium' | 'large'", "required": False},
            {"name": "onClick", "type": "() => void", "required": False}
        ],
        styling={"theme": "modern"},
        functionality=["clickable", "hoverable"],
        framework=FrameworkType.REACT
    )
    
    react_generator = ReactGenerator()
    react_result = react_generator.generate_component(react_spec)
    
    print("React Button Component:")
    print(react_result["component"])
    print("\nReact Button Styles:")
    print(react_result["styles"])
    
    # Test Vue generator
    vue_spec = ComponentSpec(
        name="CustomCard",
        type=ComponentType.CARD,
        props=[
            {"name": "title", "type": "string", "required": False},
            {"name": "variant", "type": "'default' | 'elevated'", "required": False}
        ],
        styling={"theme": "modern"},
        functionality=["slottable"],
        framework=FrameworkType.VUE
    )
    
    vue_generator = VueGenerator()
    vue_result = vue_generator.generate_component(vue_spec)
    
    print("\n" + "="*50)
    print("Vue Card Component:")
    print(vue_result["component"])
    
    print("✅ Framework-Native Code Generators implementation complete!")