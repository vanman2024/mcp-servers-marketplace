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
 * Self-contained Button component with loading states and accessibility features
 * Supports multiple variants and sizes with consistent styling
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
   * Handle click events with loading state consideration
   * Prevents clicks when loading or disabled
   */
  const handleClick = () => {
    if (!loading && !disabled && onClick) {
      onClick()
    }
  }

  /**
   * Variant styles mapping for different button appearances
   */
  const variantStyles = {
    default: 'bg-slate-900 text-slate-50 hover:bg-slate-900/90 dark:bg-slate-50 dark:text-slate-900 dark:hover:bg-slate-50/90',
    destructive: 'bg-red-500 text-slate-50 hover:bg-red-500/90 dark:bg-red-900 dark:text-slate-50 dark:hover:bg-red-900/90',
    outline: 'border border-slate-200 bg-white hover:bg-slate-100 hover:text-slate-900 dark:border-slate-800 dark:bg-slate-950 dark:hover:bg-slate-800 dark:hover:text-slate-50',
    secondary: 'bg-slate-100 text-slate-900 hover:bg-slate-100/80 dark:bg-slate-800 dark:text-slate-50 dark:hover:bg-slate-800/80',
    ghost: 'hover:bg-slate-100 hover:text-slate-900 dark:hover:bg-slate-800 dark:hover:text-slate-50',
    link: 'text-slate-900 underline-offset-4 hover:underline dark:text-slate-50'
  }

  /**
   * Size styles mapping for different button dimensions
   */
  const sizeStyles = {
    default: 'h-10 px-4 py-2',
    sm: 'h-9 rounded-md px-3',
    lg: 'h-11 rounded-md px-8',
    icon: 'h-10 w-10'
  }

  return (
    <button
      ref={ref}
      type={type}
      onClick={handleClick}
      disabled={disabled || loading}
      className={cn(
        // Base button styles
        'inline-flex items-center justify-center whitespace-nowrap rounded-md text-sm font-medium ring-offset-white transition-colors',
        // Focus styles for accessibility
        'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-slate-950 focus-visible:ring-offset-2',
        // Dark mode focus styles
        'dark:ring-offset-slate-950 dark:focus-visible:ring-slate-300',
        // Disabled state styles
        'disabled:pointer-events-none disabled:opacity-50',
        // Loading state styles
        loading && 'cursor-not-allowed',
        // Apply variant styles
        variantStyles[variant],
        // Apply size styles
        sizeStyles[size],
        // Responsive text sizing
        'text-sm sm:text-base',
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
          className="mr-2 h-4 w-4 animate-spin"
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
      {children}
    </button>
  )
})

Button.displayName = 'Button'

export default Button