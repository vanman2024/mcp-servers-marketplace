import { HTMLAttributes, ReactNode } from 'react'
import { cn } from '@/lib/utils'

interface CardProps extends HTMLAttributes<HTMLDivElement> {
  children: ReactNode
  variant?: 'default' | 'outlined' | 'elevated'
  size?: 'sm' | 'md' | 'lg'
}

interface CardHeaderProps extends HTMLAttributes<HTMLDivElement> {
  children: ReactNode
}

interface CardContentProps extends HTMLAttributes<HTMLDivElement> {
  children: ReactNode
}

interface CardFooterProps extends HTMLAttributes<HTMLDivElement> {
  children: ReactNode
}

const Card = ({ 
  children, 
  variant = 'default', 
  size = 'md', 
  className, 
  ...props 
}: CardProps) => {
  // Define variant styles for different card appearances
  const variantStyles = {
    default: 'bg-white border border-gray-200 shadow-sm',
    outlined: 'bg-white border-2 border-gray-300',
    elevated: 'bg-white shadow-lg border border-gray-100'
  }

  // Define size styles for different card dimensions
  const sizeStyles = {
    sm: 'p-4',
    md: 'p-6',
    lg: 'p-8'
  }

  return (
    <div
      className={cn(
        // Base styles with responsive design
        'rounded-lg transition-all duration-200 hover:shadow-md',
        'w-full max-w-sm sm:max-w-md md:max-w-lg lg:max-w-xl',
        variantStyles[variant],
        sizeStyles[size],
        className
      )}
      role="article"
      {...props}
    >
      {children}
    </div>
  )
}

const CardHeader = ({ children, className, ...props }: CardHeaderProps) => {
  return (
    <div
      className={cn(
        'flex flex-col space-y-1.5 pb-4 border-b border-gray-100',
        className
      )}
      {...props}
    >
      {children}
    </div>
  )
}

const CardContent = ({ children, className, ...props }: CardContentProps) => {
  return (
    <div
      className={cn('pt-4 pb-4', className)}
      {...props}
    >
      {children}
    </div>
  )
}

const CardFooter = ({ children, className, ...props }: CardFooterProps) => {
  return (
    <div
      className={cn(
        'flex items-center pt-4 border-t border-gray-100',
        className
      )}
      {...props}
    >
      {children}
    </div>
  )
}

// Card title component for semantic heading structure
interface CardTitleProps extends HTMLAttributes<HTMLHeadingElement> {
  children: ReactNode
  level?: 1 | 2 | 3 | 4 | 5 | 6
}

const CardTitle = ({ 
  children, 
  level = 3, 
  className, 
  ...props 
}: CardTitleProps) => {
  const Tag = `h${level}` as keyof JSX.IntrinsicElements

  return (
    <Tag
      className={cn(
        'text-lg font-semibold leading-none tracking-tight text-gray-900',
        'sm:text-xl md:text-2xl',
        className
      )}
      {...props}
    >
      {children}
    </Tag>
  )
}

// Card description component for subtitle text
interface CardDescriptionProps extends HTMLAttributes<HTMLParagraphElement> {
  children: ReactNode
}

const CardDescription = ({ 
  children, 
  className, 
  ...props 
}: CardDescriptionProps) => {
  return (
    <p
      className={cn(
        'text-sm text-gray-600 leading-relaxed',
        'sm:text-base',
        className
      )}
      {...props}
    >
      {children}
    </p>
  )
}

// Export all components for flexible usage
export {
  Card,
  CardHeader,
  CardContent,
  CardFooter,
  CardTitle,
  CardDescription
}

// Example usage component demonstrating the card
export default function ExampleCard() {
  return (
    <div className="p-8 bg-gray-50 min-h-screen flex items-center justify-center">
      <Card variant="elevated" size="md">
        <CardHeader>
          <CardTitle level={2}>Card Title</CardTitle>
          <CardDescription>
            This is a description of the card content. It provides context and additional information.
          </CardDescription>
        </CardHeader>
        
        <CardContent>
          <p className="text-gray-700 leading-relaxed">
            This is the main content area of the card. You can place any content here,
            including text, images, forms, or other components. The card is fully responsive
            and will adapt to different screen sizes.
          </p>
        </CardContent>
        
        <CardFooter>
          <button 
            className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition-colors focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
            aria-label="Perform card action"
          >
            Action Button
          </button>
        </CardFooter>
      </Card>
    </div>
  )
}