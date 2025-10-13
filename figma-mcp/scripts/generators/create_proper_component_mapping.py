#!/usr/bin/env python3
"""
Create proper component mapping with actual React code templates
Maps Figma components to real shadcn/ui components with executable code
"""

import json
import os
from typing import Dict, Any

def create_shadcn_component_templates() -> Dict[str, Any]:
    """Create templates for actual shadcn/ui components with working React code"""
    
    templates = {
        # BUTTON COMPONENTS
        "button": {
            "name": "Button",
            "category": "ui",
            "description": "Displays a button or a component that looks like a button",
            "template": '''import { Button } from "@/components/ui/button"

export function {{componentName}}() {
  return (
    <Button variant="{{variant}}" size="{{size}}" {{disabled}}>
      {{children}}
    </Button>
  )
}''',
            "imports": ["@/components/ui/button"],
            "dependencies": ["class-variance-authority", "clsx", "tailwind-merge"],
            "variants": {
                "variant": ["default", "destructive", "outline", "secondary", "ghost", "link"],
                "size": ["default", "sm", "lg", "icon"],
                "disabled": [False, True]
            },
            "props": ["variant", "size", "disabled", "children"],
            "example": '''<Button variant="default" size="default">Click me</Button>'''
        },
        
        # CARD COMPONENTS  
        "card": {
            "name": "Card",
            "category": "ui",
            "description": "Displays a card with header, content, and footer",
            "template": '''import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"

export function {{componentName}}() {
  return (
    <Card>
      <CardHeader>
        <CardTitle>{{title}}</CardTitle>
        <CardDescription>{{description}}</CardDescription>
      </CardHeader>
      <CardContent>
        {{content}}
      </CardContent>
      <CardFooter>
        {{footer}}
      </CardFooter>
    </Card>
  )
}''',
            "imports": ["@/components/ui/card"],
            "dependencies": ["class-variance-authority", "clsx", "tailwind-merge"],
            "props": ["title", "description", "content", "footer"],
            "example": '''<Card>
  <CardHeader>
    <CardTitle>Card Title</CardTitle>
    <CardDescription>Card description</CardDescription>
  </CardHeader>
  <CardContent>Card content</CardContent>
  <CardFooter>Card footer</CardFooter>
</Card>'''
        },
        
        # INPUT COMPONENTS
        "input": {
            "name": "Input",
            "category": "form",
            "description": "Displays a form input field",
            "template": '''import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"

export function {{componentName}}() {
  return (
    <div className="grid w-full max-w-sm items-center gap-1.5">
      <Label htmlFor="{{id}}">{{label}}</Label>
      <Input 
        type="{{type}}" 
        id="{{id}}" 
        placeholder="{{placeholder}}"
        {{disabled}}
        {{required}}
      />
    </div>
  )
}''',
            "imports": ["@/components/ui/input", "@/components/ui/label"],
            "dependencies": ["class-variance-authority", "clsx", "tailwind-merge"],
            "variants": {
                "type": ["text", "email", "password", "number", "tel", "url"],
                "disabled": [False, True],
                "required": [False, True]
            },
            "props": ["type", "id", "label", "placeholder", "disabled", "required"],
            "example": '''<Input type="email" placeholder="Email" />'''
        },
        
        # DIALOG COMPONENTS
        "dialog": {
            "name": "Dialog",
            "category": "overlay",
            "description": "A modal dialog component",
            "template": '''import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog"
import { Button } from "@/components/ui/button"

export function {{componentName}}() {
  return (
    <Dialog>
      <DialogTrigger asChild>
        <Button variant="outline">{{triggerText}}</Button>
      </DialogTrigger>
      <DialogContent className="sm:max-w-[425px]">
        <DialogHeader>
          <DialogTitle>{{title}}</DialogTitle>
          <DialogDescription>{{description}}</DialogDescription>
        </DialogHeader>
        {{content}}
        <DialogFooter>
          {{footer}}
        </DialogFooter>
      </DialogContent>
    </Dialog>
  )
}''',
            "imports": ["@/components/ui/dialog", "@/components/ui/button"],
            "dependencies": ["@radix-ui/react-dialog", "class-variance-authority", "clsx", "tailwind-merge"],
            "props": ["triggerText", "title", "description", "content", "footer"],
            "example": '''<Dialog>
  <DialogTrigger><Button>Open</Button></DialogTrigger>
  <DialogContent>
    <DialogHeader>
      <DialogTitle>Title</DialogTitle>
    </DialogHeader>
  </DialogContent>
</Dialog>'''
        },
        
        # FORM COMPONENTS
        "form": {
            "name": "Form",
            "category": "form", 
            "description": "Form component with validation",
            "template": '''import { zodResolver } from "@hookform/resolvers/zod"
import { useForm } from "react-hook-form"
import * as z from "zod"

import { Button } from "@/components/ui/button"
import {
  Form,
  FormControl,
  FormDescription,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form"
import { Input } from "@/components/ui/input"

const formSchema = z.object({
  {{schemaFields}}
})

export function {{componentName}}() {
  const form = useForm<z.infer<typeof formSchema>>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      {{defaultValues}}
    },
  })
 
  function onSubmit(values: z.infer<typeof formSchema>) {
    console.log(values)
  }

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-8">
        {{formFields}}
        <Button type="submit">Submit</Button>
      </form>
    </Form>
  )
}''',
            "imports": [
                "@/components/ui/button",
                "@/components/ui/form", 
                "@/components/ui/input",
                "react-hook-form",
                "@hookform/resolvers/zod",
                "zod"
            ],
            "dependencies": ["react-hook-form", "@hookform/resolvers/zod", "zod"],
            "props": ["schemaFields", "defaultValues", "formFields"],
            "example": '''<Form>
  <FormField name="username" render={({field}) => 
    <FormItem>
      <FormLabel>Username</FormLabel>
      <FormControl>
        <Input {...field} />
      </FormControl>
    </FormItem>
  } />
</Form>'''
        },
        
        # NAVIGATION COMPONENTS
        "navigation-menu": {
            "name": "NavigationMenu",
            "category": "navigation",
            "description": "A collection of links for navigating websites",
            "template": '''import {
  NavigationMenu,
  NavigationMenuContent,
  NavigationMenuItem,
  NavigationMenuLink,
  NavigationMenuList,
  NavigationMenuTrigger,
} from "@/components/ui/navigation-menu"

export function {{componentName}}() {
  return (
    <NavigationMenu>
      <NavigationMenuList>
        {{menuItems}}
      </NavigationMenuList>
    </NavigationMenu>
  )
}''',
            "imports": ["@/components/ui/navigation-menu"],
            "dependencies": ["@radix-ui/react-navigation-menu"],
            "props": ["menuItems"],
            "example": '''<NavigationMenu>
  <NavigationMenuList>
    <NavigationMenuItem>
      <NavigationMenuTrigger>Item One</NavigationMenuTrigger>
      <NavigationMenuContent>Content</NavigationMenuContent>
    </NavigationMenuItem>
  </NavigationMenuList>
</NavigationMenu>'''
        }
    }
    
    return templates

def create_figma_to_shadcn_mapping():
    """Map Figma component names to shadcn/ui components"""
    
    mapping = {
        # Button mappings
        "Button": "button",
        "button": "button", 
        "btn": "button",
        "CTA": "button",
        "Action": "button",
        
        # Card mappings
        "Card": "card",
        "card": "card",
        "Panel": "card",
        "Container": "card",
        
        # Input mappings
        "Input": "input",
        "input": "input", 
        "TextField": "input",
        "TextInput": "input",
        "Field": "input",
        
        # Form mappings  
        "Form": "form",
        "form": "form",
        "FormContainer": "form",
        
        # Dialog mappings
        "Dialog": "dialog",
        "Modal": "dialog",
        "Popup": "dialog",
        "Overlay": "dialog",
        
        # Navigation mappings
        "Navigation": "navigation-menu",
        "Nav": "navigation-menu", 
        "Menu": "navigation-menu",
        "NavigationMenu": "navigation-menu"
    }
    
    return mapping

def generate_component_code(template_name: str, props: Dict[str, Any]) -> str:
    """Generate actual React component code from template"""
    
    templates = create_shadcn_component_templates()
    
    if template_name not in templates:
        raise ValueError(f"Template {template_name} not found")
    
    template = templates[template_name]["template"]
    
    # Replace template variables with actual values
    for key, value in props.items():
        placeholder = "{{" + key + "}}"
        if isinstance(value, bool):
            template = template.replace(placeholder, "true" if value else "")
        else:
            template = template.replace(placeholder, str(value))
    
    return template

def main():
    """Create the proper component mapping files"""
    
    # Create templates
    templates = create_shadcn_component_templates()
    mapping = create_figma_to_shadcn_mapping()
    
    # Save templates
    with open('shadcn_component_templates.json', 'w') as f:
        json.dump(templates, f, indent=2)
    
    # Save mapping
    with open('figma_to_shadcn_mapping.json', 'w') as f:
        json.dump(mapping, f, indent=2)
    
    print(f"✅ Created {len(templates)} component templates")
    print(f"✅ Created mapping for {len(mapping)} component variations")
    
    # Test code generation
    example_props = {
        "componentName": "PrimaryButton",
        "variant": "default",
        "size": "default", 
        "disabled": "",
        "children": "Click me"
    }
    
    generated_code = generate_component_code("button", example_props)
    print("\n=== EXAMPLE GENERATED CODE ===")
    print(generated_code)

if __name__ == "__main__":
    main()