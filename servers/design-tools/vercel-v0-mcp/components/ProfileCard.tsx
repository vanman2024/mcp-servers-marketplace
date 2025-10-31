'use client'

import { useState, useRef, ChangeEvent } from 'react'
import { Card, CardContent, CardHeader } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar'
import { Camera, Loader2, AlertCircle, User, Mail, Phone, MapPin } from 'lucide-react'
import { Alert, AlertDescription } from '@/components/ui/alert'

// Shared types for the profile feature
export interface UserProfile {
  id: string
  name: string
  email: string
  phone?: string
  location?: string
  avatar?: string
  bio?: string
}

export interface AvatarUploadState {
  isUploading: boolean
  error: string | null
  preview: string | null
}

export interface ProfileCardProps {
  profile: UserProfile
  onProfileUpdate: (profile: Partial<UserProfile>) => Promise<void>
  onAvatarUpload: (file: File) => Promise<string>
  isEditing?: boolean
  onEditToggle?: () => void
  className?: string
}

export interface AvatarUploadProps {
  currentAvatar?: string
  onUpload: (file: File) => Promise<string>
  size?: 'sm' | 'md' | 'lg'
  className?: string
}

const ProfileCard = ({
  profile,
  onProfileUpdate,
  onAvatarUpload,
  isEditing = false,
  onEditToggle,
  className = ''
}: ProfileCardProps) => {
  const [isUpdating, setIsUpdating] = useState(false)
  const [updateError, setUpdateError] = useState<string | null>(null)
  const [avatarState, setAvatarState] = useState<AvatarUploadState>({
    isUploading: false,
    error: null,
    preview: null
  })
  const [formData, setFormData] = useState({
    name: profile.name,
    email: profile.email,
    phone: profile.phone || '',
    location: profile.location || '',
    bio: profile.bio || ''
  })

  const fileInputRef = useRef<HTMLInputElement>(null)

  // Handle avatar upload
  const handleAvatarUpload = async (event: ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0]
    if (!file) return

    // Validate file type and size
    if (!file.type.startsWith('image/')) {
      setAvatarState(prev => ({ ...prev, error: 'Please select an image file' }))
      return
    }

    if (file.size > 5 * 1024 * 1024) { // 5MB limit
      setAvatarState(prev => ({ ...prev, error: 'File size must be less than 5MB' }))
      return
    }

    setAvatarState(prev => ({ ...prev, isUploading: true, error: null }))

    try {
      // Create preview
      const preview = URL.createObjectURL(file)
      setAvatarState(prev => ({ ...prev, preview }))

      // Upload file
      const avatarUrl = await onAvatarUpload(file)
      
      // Update profile with new avatar
      await onProfileUpdate({ avatar: avatarUrl })
      
      setAvatarState(prev => ({ ...prev, isUploading: false, preview: null }))
    } catch (error) {
      setAvatarState(prev => ({
        ...prev,
        isUploading: false,
        error: error instanceof Error ? error.message : 'Failed to upload avatar',
        preview: null
      }))
    }

    // Reset file input
    if (fileInputRef.current) {
      fileInputRef.current.value = ''
    }
  }

  // Handle profile update
  const handleProfileUpdate = async () => {
    setIsUpdating(true)
    setUpdateError(null)

    try {
      await onProfileUpdate(formData)
      onEditToggle?.()
    } catch (error) {
      setUpdateError(error instanceof Error ? error.message : 'Failed to update profile')
    } finally {
      setIsUpdating(false)
    }
  }

  // Handle form input changes
  const handleInputChange = (field: keyof typeof formData, value: string) => {
    setFormData(prev => ({ ...prev, [field]: value }))
  }

  // Get user initials for avatar fallback
  const getUserInitials = (name: string) => {
    return name
      .split(' ')
      .map(part => part.charAt(0))
      .join('')
      .toUpperCase()
      .slice(0, 2)
  }

  return (
    <Card className={`w-full max-w-2xl mx-auto ${className}`}>
      <CardHeader className="text-center pb-4">
        <div className="relative inline-block">
          <Avatar className="w-24 h-24 mx-auto">
            <AvatarImage 
              src={avatarState.preview || profile.avatar} 
              alt={`${profile.name}'s avatar`}
            />
            <AvatarFallback className="text-lg font-semibold">
              {getUserInitials(profile.name)}
            </AvatarFallback>
          </Avatar>
          
          {/* Avatar upload overlay */}
          <Button
            variant="outline"
            size="sm"
            className="absolute -bottom-2 -right-2 rounded-full w-8 h-8 p-0"
            onClick={() => fileInputRef.current?.click()}
            disabled={avatarState.isUploading}
            aria-label="Upload new avatar"
          >
            {avatarState.isUploading ? (
              <Loader2 className="w-4 h-4 animate-spin" />
            ) : (
              <Camera className="w-4 h-4" />
            )}
          </Button>
          
          <input
            ref={fileInputRef}
            type="file"
            accept="image/*"
            onChange={handleAvatarUpload}
            className="hidden"
            aria-label="Select avatar image"
          />
        </div>

        {/* Avatar upload error */}
        {avatarState.error && (
          <Alert variant="destructive" className="mt-4">
            <AlertCircle className="h-4 w-4" />
            <AlertDescription>{avatarState.error}</AlertDescription>
          </Alert>
        )}
      </CardHeader>

      <CardContent className="space-y-6">
        {/* Profile form */}
        <div className="grid gap-4">
          {/* Name field */}
          <div className="space-y-2">
            <Label htmlFor="name" className="flex items-center gap-2">
              <User className="w-4 h-4" />
              Name
            </Label>
            {isEditing ? (
              <Input
                id="name"
                value={formData.name}
                onChange={(e) => handleInputChange('name', e.target.value)}
                placeholder="Enter your name"
                required
              />
            ) : (
              <p className="text-sm font-medium px-3 py-2 bg-muted rounded-md">
                {profile.name}
              </p>
            )}
          </div>

          {/* Email field */}
          <div className="space-y-2">
            <Label htmlFor="email" className="flex items-center gap-2">
              <Mail className="w-4 h-4" />
              Email
            </Label>
            {isEditing ? (
              <Input
                id="email"
                type="email"
                value={formData.email}
                onChange={(e) => handleInputChange('email', e.target.value)}
                placeholder="Enter your email"
                required
              />
            ) : (
              <p className="text-sm font-medium px-3 py-2 bg-muted rounded-md">
                {profile.email}
              </p>
            )}
          </div>

          {/* Phone field */}
          <div className="space-y-2">
            <Label htmlFor="phone" className="flex items-center gap-2">
              <Phone className="w-4 h-4" />
              Phone
            </Label>
            {isEditing ? (
              <Input
                id="phone"
                type="tel"
                value={formData.phone}
                onChange={(e) => handleInputChange('phone', e.target.value)}
                placeholder="Enter your phone number"
              />
            ) : (
              <p className="text-sm font-medium px-3 py-2 bg-muted rounded-md">
                {profile.phone || 'Not provided'}
              </p>
            )}
          </div>

          {/* Location field */}
          <div className="space-y-2">
            <Label htmlFor="location" className="flex items-center gap-2">
              <MapPin className="w-4 h-4" />
              Location
            </Label>
            {isEditing ? (
              <Input
                id="location"
                value={formData.location}
                onChange={(e) => handleInputChange('location', e.target.value)}
                placeholder="Enter your location"
              />
            ) : (
              <p className="text-sm font-medium px-3 py-2 bg-muted rounded-md">
                {profile.location || 'Not provided'}
              </p>
            )}
          </div>

          {/* Bio field */}
          <div className="space-y-2">
            <Label htmlFor="bio">Bio</Label>
            {isEditing ? (
              <textarea
                id="bio"
                value={formData.bio}
                onChange={(e) => handleInputChange('bio', e.target.value)}
                placeholder="Tell us about yourself"
                className="flex min-h-[80px] w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50 resize-none"
                rows={3}
              />
            ) : (
              <p className="text-sm font-medium px-3 py-2 bg-muted rounded-md min-h-[80px]">
                {profile.bio || 'No bio provided'}
              </p>
            )}
          </div>
        </div>

        {/* Update error */}
        {updateError && (
          <Alert variant="destructive">
            <AlertCircle className="h-4 w-4" />
            <AlertDescription>{updateError}</AlertDescription>
          </Alert>
        )}

        {/* Action buttons */}
        <div className="flex gap-3 pt-4">
          {isEditing ? (
            <>
              <Button
                onClick={handleProfileUpdate}
                disabled={isUpdating}
                className="flex-1"
              >
                {isUpdating ? (
                  <>
                    <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                    Saving...
                  </>
                ) : (
                  'Save Changes'
                )}
              </Button>
              <Button
                variant="outline"
                onClick={onEditToggle}
                disabled={isUpdating}
              >
                Cancel
              </Button>
            </>
          ) : (
            <Button onClick={onEditToggle} className="flex-1">
              Edit Profile
            </Button>
          )}
        </div>
      </CardContent>
    </Card>
  )
}

export default ProfileCard