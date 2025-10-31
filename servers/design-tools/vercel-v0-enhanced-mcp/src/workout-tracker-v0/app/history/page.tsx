import { WorkoutHistory } from '@/components/workout-history'

export default function HistoryPage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Workout History</h1>
        <p className="text-muted-foreground">
          View all your past workouts and track your progress
        </p>
      </div>
      <WorkoutHistory />
    </div>
  )
}