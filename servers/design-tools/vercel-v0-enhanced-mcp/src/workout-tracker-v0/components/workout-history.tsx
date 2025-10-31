'use client'

import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { useWorkouts } from '@/hooks/use-workouts'
import { formatDate } from '@/lib/utils'
import { Calendar, Trash2, Dumbbell } from 'lucide-react'

export function WorkoutHistory() {
  const { workouts, removeWorkout } = useWorkouts()

  if (workouts.length === 0) {
    return (
      <Card>
        <CardContent className="py-12">
          <div className="text-center">
            <Dumbbell className="h-16 w-16 mx-auto text-muted-foreground mb-4" />
            <h3 className="text-lg font-semibold mb-2">No workouts yet</h3>
            <p className="text-muted-foreground">
              Start logging your workouts to see your history here.
            </p>
          </div>
        </CardContent>
      </Card>
    )
  }

  return (
    <div className="space-y-4">
      {workouts.map((workout, workoutIndex) => (
        <Card key={workoutIndex}>
          <CardHeader>
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-2">
                <Calendar className="h-5 w-5 text-muted-foreground" />
                <CardTitle className="text-lg">
                  {formatDate(workout.date)}
                </CardTitle>
              </div>
              <Button
                variant="ghost"
                size="sm"
                onClick={() => removeWorkout(workoutIndex)}
                className="text-destructive hover:text-destructive"
              >
                <Trash2 className="h-4 w-4" />
              </Button>
            </div>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {workout.exercises.map((exercise, exerciseIndex) => (
                <div key={exerciseIndex} className="border rounded-lg p-4">
                  <h4 className="font-semibold mb-3">{exercise.name}</h4>
                  <div className="space-y-2">
                    <div className="grid grid-cols-3 gap-4 text-sm font-medium text-muted-foreground">
                      <span>Set</span>
                      <span>Reps</span>
                      <span>Weight (lbs)</span>
                    </div>
                    {exercise.sets.map((set, setIndex) => (
                      <div key={setIndex} className="grid grid-cols-3 gap-4 text-sm">
                        <span>{setIndex + 1}</span>
                        <span>{set.reps}</span>
                        <span>{set.weight}</span>
                      </div>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      ))}
    </div>
  )
}