'use client'

import { useState } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Plus, Trash2 } from 'lucide-react'
import { useWorkouts } from '@/hooks/use-workouts'
import type { Exercise, WorkoutSet } from '@/types/workout'

export function WorkoutLogger() {
  const { addWorkout } = useWorkouts()
  const [exercises, setExercises] = useState<Exercise[]>([
    { name: '', sets: [{ reps: 0, weight: 0 }] }
  ])

  const addExercise = () => {
    setExercises([...exercises, { name: '', sets: [{ reps: 0, weight: 0 }] }])
  }

  const removeExercise = (index: number) => {
    setExercises(exercises.filter((_, i) => i !== index))
  }

  const updateExercise = (index: number, field: keyof Exercise, value: string) => {
    const updated = [...exercises]
    updated[index] = { ...updated[index], [field]: value }
    setExercises(updated)
  }

  const addSet = (exerciseIndex: number) => {
    const updated = [...exercises]
    updated[exerciseIndex].sets.push({ reps: 0, weight: 0 })
    setExercises(updated)
  }

  const removeSet = (exerciseIndex: number, setIndex: number) => {
    const updated = [...exercises]
    updated[exerciseIndex].sets = updated[exerciseIndex].sets.filter((_, i) => i !== setIndex)
    setExercises(updated)
  }

  const updateSet = (exerciseIndex: number, setIndex: number, field: keyof WorkoutSet, value: number) => {
    const updated = [...exercises]
    updated[exerciseIndex].sets[setIndex] = {
      ...updated[exerciseIndex].sets[setIndex],
      [field]: value
    }
    setExercises(updated)
  }

  const saveWorkout = () => {
    const validExercises = exercises.filter(ex => ex.name.trim() !== '')
    if (validExercises.length === 0) return

    addWorkout({
      date: new Date().toISOString(),
      exercises: validExercises
    })

    setExercises([{ name: '', sets: [{ reps: 0, weight: 0 }] }])
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>Log Workout</CardTitle>
      </CardHeader>
      <CardContent className="space-y-6">
        {exercises.map((exercise, exerciseIndex) => (
          <div key={exerciseIndex} className="space-y-4 p-4 border rounded-lg">
            <div className="flex items-center justify-between">
              <div className="flex-1">
                <Label htmlFor={`exercise-${exerciseIndex}`}>Exercise Name</Label>
                <Input
                  id={`exercise-${exerciseIndex}`}
                  value={exercise.name}
                  onChange={(e) => updateExercise(exerciseIndex, 'name', e.target.value)}
                  placeholder="e.g., Bench Press"
                  className="mt-1"
                />
              </div>
              {exercises.length > 1 && (
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() => removeExercise(exerciseIndex)}
                  className="ml-2"
                >
                  <Trash2 className="h-4 w-4" />
                </Button>
              )}
            </div>

            <div className="space-y-2">
              <Label>Sets</Label>
              {exercise.sets.map((set, setIndex) => (
                <div key={setIndex} className="flex items-center space-x-2">
                  <span className="text-sm text-muted-foreground w-8">
                    {setIndex + 1}.
                  </span>
                  <div className="flex-1">
                    <Input
                      type="number"
                      value={set.reps || ''}
                      onChange={(e) => updateSet(exerciseIndex, setIndex, 'reps', parseInt(e.target.value) || 0)}
                      placeholder="Reps"
                      min="0"
                    />
                  </div>
                  <div className="flex-1">
                    <Input
                      type="number"
                      value={set.weight || ''}
                      onChange={(e) => updateSet(exerciseIndex, setIndex, 'weight', parseFloat(e.target.value) || 0)}
                      placeholder="Weight (lbs)"
                      min="0"
                      step="0.5"
                    />
                  </div>
                  {exercise.sets.length > 1 && (
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => removeSet(exerciseIndex, setIndex)}
                    >
                      <Trash2 className="h-4 w-4" />
                    </Button>
                  )}
                </div>
              ))}
              <Button
                variant="outline"
                size="sm"
                onClick={() => addSet(exerciseIndex)}
                className="w-full"
              >
                <Plus className="h-4 w-4 mr-2" />
                Add Set
              </Button>
            </div>
          </div>
        ))}

        <div className="flex space-x-2">
          <Button variant="outline" onClick={addExercise} className="flex-1">
            <Plus className="h-4 w-4 mr-2" />
            Add Exercise
          </Button>
          <Button onClick={saveWorkout} className="flex-1">
            Save Workout
          </Button>
        </div>
      </CardContent>
    </Card>
  )
}