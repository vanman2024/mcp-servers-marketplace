import { Suspense } from 'react'
import { MetricsOverview } from '@/components/metrics-overview'
import { AgentGrid } from '@/components/agent-grid'
import { ActivityFeed } from '@/components/activity-feed'
import { ResourceUsage } from '@/components/resource-usage'
import { BranchOverview } from '@/components/branch-overview'
import { LoadingSkeleton } from '@/components/loading-skeleton'

export default function Dashboard() {
  return (
    <div className="min-h-screen bg-gray-950 text-white">
      <div className="container mx-auto p-6 space-y-6">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">
              Agent Development Control
            </h1>
            <p className="text-gray-400 mt-1">
              Real-time monitoring of parallel development agents
            </p>
          </div>
          <div className="flex items-center space-x-2">
            <div className="w-3 h-3 bg-green-500 rounded-full animate-pulse"></div>
            <span className="text-sm text-gray-400">System Online</span>
          </div>
        </div>

        {/* Metrics Overview */}
        <Suspense fallback={<LoadingSkeleton />}>
          <MetricsOverview />
        </Suspense>

        {/* Main Content Grid */}
        <div className="grid grid-cols-1 xl:grid-cols-4 gap-6">
          {/* Agent Grid - Takes up 3 columns */}
          <div className="xl:col-span-3">
            <Suspense fallback={<LoadingSkeleton />}>
              <AgentGrid />
            </Suspense>
          </div>

          {/* Right Sidebar */}
          <div className="space-y-6">
            <Suspense fallback={<LoadingSkeleton />}>
              <ActivityFeed />
            </Suspense>
            <Suspense fallback={<LoadingSkeleton />}>
              <ResourceUsage />
            </Suspense>
          </div>
        </div>

        {/* Branch Overview */}
        <Suspense fallback={<LoadingSkeleton />}>
          <BranchOverview />
        </Suspense>
      </div>
    </div>
  )
}