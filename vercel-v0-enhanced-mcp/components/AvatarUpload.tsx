'use client'

import { useState, useRef, ChangeEvent } from 'react'
// Self-contained avatar components
const Avatar = ({ children, className }: { children: React.ReactNode; className?: string }) => (
  <div className={cn('relative flex h-10 w-10 shrink-0 overflow-hidden rounded-full', className)}>
    {children}
  </div>
)

const AvatarImage = ({ src, alt }: { src?: string; alt?: string }) => (
  src ? <img className="aspect-square h-full w-full" src={src} alt={alt} /> : null
)

const AvatarFallback = ({ children, className }: { children: React.ReactNode; className?: string }) => (
  <div className={cn('flex h-full w-full items-center justify-center rounded-full bg-muted', className)}>
    {children}
  </div>
)

// Self-contained button component
const Button = ({ children, onClick, disabled, variant = 'default', className, ...props }: {
  children: React.ReactNode
  onClick?: () => void
  disabled?: boolean
  variant?: 'default' | 'outline' | 'ghost'
  className?: string
  [key: string]: any
}) => {
  const variantStyles = {
    default: 'bg-primary text-primary-foreground hover:bg-primary/90',
    outline: 'border border-input bg-background hover:bg-accent hover:text-accent-foreground',
    ghost: 'hover:bg-accent hover:text-accent-foreground'
  }
  
  return (
    <button
      onClick={onClick}
      disabled={disabled}
      className={cn(
        'inline-flex items-center justify-center whitespace-nowrap rounded-md text-sm font-medium transition-colors',
        'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2',
        'disabled:pointer-events-none disabled:opacity-50 h-10 px-4 py-2',
        variantStyles[variant],
        className
      )}
      {...props}
    >
      {children}
    </button>
  )
}

// Self-contained alert components
const Alert = ({ children, className }: { children: React.ReactNode; className?: string }) => (
  <div className={cn('relative w-full rounded-lg border p-4', className)}>
    {children}
  </div>
)

const AlertDescription = ({ children, className }: { children: React.ReactNode; className?: string }) => (
  <div className={cn('text-sm [&_p]:leading-relaxed', className)}>
    {children}
  </div>
)
import { Loader2, Upload, User, X } from 'lucide-react'
import { cn } from '@/lib/utils'

// Exported types for other components to use
export interface AvatarUploadProps {
  currentAvatar?: string
  onAvatarChange?: (file: File | null, previewUrl: string | null) => void
  onUploadComplete?: (avatarUrl: string) => void
  onUploadError?: (error: string) => void
  maxFileSize?: number // in bytes
  acceptedFileTypes?: string[]
  disabled?: boolean
  className?: string
}

export interface UploadState {
  isUploading: boolean
  error: string | null
  previewUrl: string | null
}

export interface AvatarData {
  file: File | null
  url: string | null
  isDefault: boolean
}

const AvatarUpload = ({
  currentAvatar,
  onAvatarChange,
  onUploadComplete,
  onUploadError,
  maxFileSize = 5 * 1024 * 1024, // 5MB default
  acceptedFileTypes = ['image/jpeg', 'image/png', 'image/webp'],
  disabled = false,
  className
}: AvatarUploadProps) => {
  const [uploadState, setUploadState] = useState<UploadState>({
    isUploading: false,
    error: null,
    previewUrl: currentAvatar || null
  })

  const fileInputRef = useRef<HTMLInputElement>(null)

  // Validate file before processing
  const validateFile = (file: File): string | null => {
    if (!acceptedFileTypes.includes(file.type)) {
      return `Please select a valid image file (${acceptedFileTypes.map(type => type.split('/')[1]).join(', ')})`
    }

    if (file.size > maxFileSize) {
      const maxSizeMB = maxFileSize / (1024 * 1024)
      return `File size must be less than ${maxSizeMB}MB`
    }

    return null
  }

  // Handle file selection and preview
  const handleFileSelect = (event: ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0]
    
    if (!file) return

    const validationError = validateFile(file)
    if (validationError) {
      setUploadState(prev => ({
        ...prev,
        error: validationError
      }))
      return
    }

    // Clear any previous errors
    setUploadState(prev => ({
      ...prev,
      error: null
    }))

    // Create preview URL
    const previewUrl = URL.createObjectURL(file)
    
    setUploadState(prev => ({
      ...prev,
      previewUrl
    }))

    // Notify parent component of file selection
    onAvatarChange?.(file, previewUrl)
  }

  // Simulate upload process (replace with actual upload logic)
  const handleUpload = async () => {
    if (!fileInputRef.current?.files?.[0]) return

    const file = fileInputRef.current.files[0]
    
    setUploadState(prev => ({
      ...prev,
      isUploading: true,
      error: null
    }))

    try {
      // Simulate upload delay
      await new Promise(resolve => setTimeout(resolve, 2000))
      
      // In a real implementation, you would upload to your server/cloud storage
      // const uploadedUrl = await uploadToServer(file)
      const uploadedUrl = uploadState.previewUrl || ''
      
      setUploadState(prev => ({
        ...prev,
        isUploading: false
      }))

      onUploadComplete?.(uploadedUrl)
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Upload failed'
      
      setUploadState(prev => ({
        ...prev,
        isUploading: false,
        error: errorMessage
      }))

      onUploadError?.(errorMessage)
    }
  }

  // Remove current avatar
  const handleRemoveAvatar = () => {
    if (uploadState.previewUrl && uploadState.previewUrl !== currentAvatar) {
      URL.revokeObjectURL(uploadState.previewUrl)
    }

    setUploadState({
      isUploading: false,
      error: null,
      previewUrl: null
    })

    if (fileInputRef.current) {
      fileInputRef.current.value = ''
    }

    onAvatarChange?.(null, null)
  }

  // Trigger file input click
  const handleSelectClick = () => {
    if (!disabled && fileInputRef.current) {
      fileInputRef.current.click()
    }
  }

  const hasPreview = uploadState.previewUrl !== null
  const showUploadButton = hasPreview && uploadState.previewUrl !== currentAvatar && !uploadState.isUploading

  return (
    <div className={cn('flex flex-col items-center space-y-4', className)}>
      {/* Avatar Display */}
      <div className="relative group">
        <Avatar className="h-24 w-24 md:h-32 md:w-32 border-2 border-muted">
          <AvatarImage 
            src={uploadState.previewUrl || undefined} 
            alt="Profile avatar"
            className="object-cover"
          />
          <AvatarFallback className="bg-muted">
            <User className="h-8 w-8 md:h-12 md:w-12 text-muted-foreground" />
          </AvatarFallback>
        </Avatar>

        {/* Remove button overlay */}
        {hasPreview && !disabled && (
          <Button
            variant="destructive"
            size="sm"
            className="absolute -top-2 -right-2 h-6 w-6 rounded-full p-0 opacity-0 group-hover:opacity-100 transition-opacity"
            onClick={handleRemoveAvatar}
            disabled={uploadState.isUploading}
            aria-label="Remove avatar"
          >
            <X className="h-3 w-3" />
          </Button>
        )}

        {/* Loading overlay */}
        {uploadState.isUploading && (
          <div className="absolute inset-0 bg-black/50 rounded-full flex items-center justify-center">
            <Loader2 className="h-6 w-6 text-white animate-spin" />
          </div>
        )}
      </div>

      {/* Action Buttons */}
      <div className="flex flex-col sm:flex-row gap-2 w-full max-w-xs">
        <Button
          variant="outline"
          onClick={handleSelectClick}
          disabled={disabled || uploadState.isUploading}
          className="flex-1"
        >
          <Upload className="h-4 w-4 mr-2" />
          {hasPreview ? 'Change' : 'Select'} Avatar
        </Button>

        {showUploadButton && (
          <Button
            onClick={handleUpload}
            disabled={disabled || uploadState.isUploading}
            className="flex-1"
          >
            {uploadState.isUploading ? (
              <>
                <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                Uploading...
              </>
            ) : (
              'Upload'
            )}
          </Button>
        )}
      </div>

      {/* Hidden file input */}
      <input
        ref={fileInputRef}
        type="file"
        accept={acceptedFileTypes.join(',')}
        onChange={handleFileSelect}
        className="hidden"
        disabled={disabled}
        aria-label="Select avatar image file"
      />

      {/* Error display */}
      {uploadState.error && (
        <Alert variant="destructive" className="w-full max-w-md">
          <AlertDescription>{uploadState.error}</AlertDescription>
        </Alert>
      )}

      {/* Upload guidelines */}
      <div className="text-xs text-muted-foreground text-center max-w-md">
        <p>
          Supported formats: {acceptedFileTypes.map(type => type.split('/')[1].toUpperCase()).join(', ')}
        </p>
        <p>
          Maximum file size: {(maxFileSize / (1024 * 1024)).toFixed(1)}MB
        </p>
      </div>
    </div>
  )
}

export default AvatarUpload