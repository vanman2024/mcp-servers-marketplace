import { Card, CardContent, CardHeader } from '@/components/ui/card'

export function LoadingSkeleton() {
  return (
    <div className="space-y-6">
      {/* Metrics Overview Skeleton */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {[...Array(4)].map((_, i) => (
          <Card key={i} className="bg-gray-900/50 border-gray-800">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div className="space-y-2">
                  <div className="h-4 bg-gray-700 rounded animate-pulse w-20"></div>
                  <div className="h-8 bg-gray-700 rounded animate-pulse w-16"></div>
                </div>
                <div className="h-12 w-12 bg-gray-700 rounded-lg animate-pulse"></div>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Main Content Skeleton */}
      <div className="grid grid-cols-1 xl:grid-cols-4 gap-6">
        {/* Agent Grid Skeleton */}
        <div className="xl:col-span-3 space-y-4">
          <div className="h-6 bg-gray-700 rounded animate-pulse w-32"></div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {[...Array(6)].map((_, i) => (
              <Card key={i} className="bg-gray-900/50 border-gray-800">
                <CardHeader className="pb-3">
                  <div className="flex items-center justify-between">
                    <div className="h-5 bg-gray-700 rounded animate-pulse w-20"></div>
                    <div className="h-6 bg-gray-700 rounded-full animate-pulse w-16"></div>
                  </div>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="h-4 bg-gray-700 rounded animate-pulse w-full"></div>
                  <div className="space-y-2">
                    <div className="h-4 bg-gray-700 rounded animate-pulse w-3/4"></div>
                    <div className="h-2 bg-gray-700 rounded animate-pulse w-full"></div>
                  </div>
                  <div className="flex justify-between">
                    <div className="h-3 bg-gray-700 rounded animate-pulse w-16"></div>
                    <div className="h-3 bg-gray-700 rounded animate-pulse w-20"></div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>

        {/* Sidebar Skeleton */}
        <div className="space-y-6">
          {/* Activity Feed Skeleton */}
          <Card className="bg-gray-900/50 border-gray-800">
            <CardHeader>
              <div className="h-5 bg-gray-700 rounded animate-pulse w-32"></div>
            </CardHeader>
            <CardContent className="space-y-4">
              {[...Array(6)].map((_, i) => (
                <div key={i} className="flex items-start space-x-3 p-3 rounded-lg bg-gray-