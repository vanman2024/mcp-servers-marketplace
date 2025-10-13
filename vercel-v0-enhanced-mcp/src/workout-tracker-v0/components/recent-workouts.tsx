'use client'

import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { useWorkouts } from '@/hooks/use-workouts'
import { formatDate } from '@/lib/utils'
import { Calendar, Dumbbell } from 'lucide-react'

export function RecentWorkouts() {
  const { workouts } = useWorkouts()
  const recentWorkouts = workouts.slice(0, 5)

  if (recentWorkouts.length === 0) {
    return (
      <Card>
        <CardHeader>
          <CardTitle>Recent Workouts</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="text-center py-8">
            <Dumbbell className="h-12 w-12 mx-auto text-muted-foreground mb-4" />
            <p className="text-muted-foreground">No workouts logged yet</p>
            <p className="text-sm text-muted-foreground">Start by logging your first workout!</p>
          </div>
        </CardContent>
      </Card>
    )
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>Recent Workouts</CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        {recentWorkouts.map((workout, index) => (
          <div key={index} className="border rounded-lg p-4">
            <div className="flex items-center justify-between mb-3">
              <div className="flex items-center space-x-2">
                <Calendar className="h-4 w-4 text-muted-foreground" />
                <span className="text-sm font-medium">
                  {formatDate(workout.date)}
                </span>
              </div>
              <span className="text-sm text-muted-foreground">
                {workout.exercises.length} exercise{workout.exercises.length !== 1 ? 's' : ''}
              </span>
            </div>
            <div className="space-y-2">
              {workout.exercises.map((exercise, exerciseIndex) => (
                <div key={exerciseIndex} className="text-sm">
                  <span className="font-medium">{exercise.name}</span>
                  <span className="text-muted-foreground ml-2">
                    {exercise.sets.length} set{exercise.sets.length !== 1 ? 's' : ''}
                  </span>
                </div>
              ))}
            </div>
          </div>
        ))}
      </CardContent>
    </Card>
  )
}