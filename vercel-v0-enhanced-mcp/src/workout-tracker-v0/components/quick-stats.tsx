'use client'

import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { useWorkouts } from '@/hooks/use-workouts'
import { TrendingUp, Calendar, Dumbbell, Target } from 'lucide-react'

export function QuickStats() {
  const { workouts } = useWorkouts()

  const totalWorkouts = workouts.length
  const totalExercises = workouts.reduce((sum, workout) => sum + workout.exercises.length, 0)
  const totalSets = workouts.reduce((sum, workout) => 
    sum + workout.exercises.reduce((exerciseSum, exercise) => exerciseSum + exercise.sets.length, 0), 0
  )

  const thisWeekWorkouts = workouts.filter(workout => {
    const workoutDate = new Date(workout.date)
    const now = new Date()
    const weekAgo = new Date(now.getTime() - 7 * 24 * 60 * 60 * 1000)
    return workoutDate >= weekAgo
  }).length

  const stats = [
    {
      title: 'Total Workouts',
      value: totalWorkouts,
      icon: Calendar,
      color: 'text-blue-600'
    },
    {
      title: 'This Week',
      value: thisWeekWorkouts,
      icon: TrendingUp,
      color: 'text-green-600'
    },
    {
      title: 'Total Exercises',
      value: totalExercises,
      icon: Dumbbell,
      color: 'text-purple-600'
    },
    {
      title: 'Total Sets',
      value: totalSets,
      icon: Target,
      color: 'text-orange-600'
    }
  ]

  return (
    <Card>
      <CardHeader>
        <CardTitle>Quick Stats</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="grid grid-cols-2 gap-4">
          {stats.map((stat, index) => {
            const Icon = stat.icon
            return (
              <div key={index} className="text-center p-4 border rounded-lg">
                <Icon className={`h-8 w-8 mx-auto mb-2 ${stat.color}`} />
                <div className="text-2xl font-bold">{stat.value}</div>
                <div className="text-sm text-muted-foreground">{stat.title}</div>
              </div>
            )
          })}
        </div>
      </CardContent>
    </Card>
  )
}