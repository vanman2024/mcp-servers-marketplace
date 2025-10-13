import { ButtonHTMLAttributes, ReactNode, forwardRef } from 'react'
import { cn } from '@/lib/utils'

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  children: ReactNode
  variant?: 'default' | 'destructive' | 'outline' | 'secondary' | 'ghost' | 'link'
  size?: 'default' | 'sm' | 'lg' | 'icon'
  loading?: boolean
  onClick?: () => void
  className?: string
}

/**
 * A comprehensive button component with multiple variants, sizes, and loading states.
 * Built with accessibility and responsive design in mind.
 */
const Button = forwardRef<HTMLButtonElement, ButtonProps>(({
  children,
  variant = 'default',
  size = 'default',
  loading = false,
  onClick,
  className,
  disabled,
  type = 'button',
  ...props
}, ref) => {
  /**
   * Handle click events with loading and disabled state consideration
   * Prevents multiple clicks during loading state
   */
  const handleClick = () => {
    if (!loading && !disabled && onClick) {
      onClick()
    }
  }

  /**
   * Base button styles that apply to all variants
   */
  const baseStyles = [
    // Layout and interaction
    'inline-flex items-center justify-center whitespace-nowrap rounded-md',
    'font-medium transition-colors duration-200 ease-in-out',
    'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2',
    'disabled:pointer-events-none disabled:opacity-50',
    // Responsive text sizing
    'text-sm sm:text-base',
  ]

  /**
   * Variant-specific styles for different button appearances
   */
  const variantStyles = {
    default: [
      'bg-primary text-primary-foreground hover:bg-primary/90',
      'bg-slate-900 text-slate-50 hover:bg-slate-900/90',
      'focus-visible:ring-slate-950'
    ],
    destructive: [
      'bg-destructive text-destructive-foreground hover:bg-destructive/90',
      'bg-red-500 text-slate-50 hover:bg-red-500/90',
      'focus-visible:ring-red-500'
    ],
    outline: [
      'border border-input bg-background hover:bg-accent hover:text-accent-foreground',
      'border-slate-200 bg-white hover:bg-slate-100 hover:text-slate-900',
      'focus-visible:ring-slate-950'
    ],
    secondary: [
      'bg-secondary text-secondary-foreground hover:bg-secondary/80',
      'bg-slate-100 text-slate-900 hover:bg-slate-100/80',
      'focus-visible:ring-slate-950'
    ],
    ghost: [
      'hover:bg-accent hover:text-accent-foreground',
      'hover:bg-slate-100 hover:text-slate-900',
      'focus-visible:ring-slate-950'
    ],
    link: [
      'text-primary underline-offset-4 hover:underline',
      'text-slate-900 hover:underline',
      'focus-visible:ring-slate-950'
    ]
  }

  /**
   * Size-specific styles for different button dimensions
   */
  const sizeStyles = {
    default: 'h-10 px-4 py-2 sm:px-6 sm:py-3',
    sm: 'h-9 rounded-md px-3 text-xs sm:text-sm',
    lg: 'h-11 rounded-md px-8 text-base sm:text-lg',
    icon: 'h-10 w-10 p-0'
  }

  /**
   * Loading state styles
   */
  const loadingStyles = loading ? [
    'cursor-not-allowed',
    'relative',
    // Slightly reduce opacity when loading
    'opacity-80'
  ] : []

  return (
    <button
      ref={ref}
      type={type}
      onClick={handleClick}
      disabled={disabled || loading}
      className={cn(
        baseStyles,
        variantStyles[variant],
        sizeStyles[size],
        loadingStyles,
        className
      )}
      aria-label={typeof children === 'string' ? children : undefined}
      aria-disabled={disabled || loading}
      aria-busy={loading}
      {...props}
    >
      {/* Loading spinner with proper accessibility */}
      {loading && (
        <svg
          className="mr-2 h-4 w-4 animate-spin shrink-0"
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 24 24"
          aria-hidden="true"
          role="img"
          aria-label="Loading"
        >
          <circle
            className="opacity-25"
            cx="12"
            cy="12"
            r="10"
            stroke="currentColor"
            strokeWidth="4"
          />
          <path
            className="opacity-75"
            fill="currentColor"
            d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
          />
        </svg>
      )}
      
      {/* Button content with proper spacing when loading */}
      <span className={cn(loading && size !== 'icon' && 'ml-1')}>
        {children}
      </span>
    </button>
  )
})

Button.displayName = 'Button'

export default Button