import { WorkoutLogger } from '@/components/workout-logger'
import { RecentWorkouts } from '@/components/recent-workouts'
import { QuickStats } from '@/components/quick-stats'

export default function HomePage() {
  return (
    <div className="space-y-8">
      <div className="text-center">
        <h1 className="text-4xl font-bold tracking-tight">Workout Tracker</h1>
        <p className="text-muted-foreground mt-2">
          Log your workouts and track your progress
        </p>
      </div>
      
      <div className="grid gap-8 lg:grid-cols-2">
        <div className="space-y-6">
          <WorkoutLogger />
          <QuickStats />
        </div>
        <RecentWorkouts />
      </div>
    </div>
  )
}