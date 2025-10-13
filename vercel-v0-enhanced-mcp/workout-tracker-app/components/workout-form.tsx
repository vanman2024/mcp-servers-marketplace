'use client'

import { useState, useEffect } from 'react'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Card, CardContent } from '@/components/ui/card'
import { Workout } from '@/lib/types'
import { exerciseData } from '@/lib/exercise-data'
import { Command, CommandEmpty, CommandGroup, CommandInput, CommandItem, CommandList } from '@/components/ui/command'
import { Popover, PopoverContent, PopoverTrigger } from '@/components/ui/popover'
import { Check, ChevronsUpDown, X } from 'lucide-react'
import { cn } from '@/lib/utils'

interface WorkoutFormProps {
  onSubmit: (workout: Omit<Workout, 'id' | 'date'> | Workout) => void
  initialData?: Workout | null
  onCancel?: () => void
}

export function WorkoutForm({ onSubmit, initialData, onCancel }: WorkoutFormProps) {
  const [exercise, setExercise] = useState('')
  const [sets, setSets] = useState('')
  const [reps, setReps] = useState('')
  const [weight, setWeight] = useState('')
  const [open, setOpen] = useState(false)

  useEffect(() => {
    if (initialData) {
      setExercise(initialData.exercise)
      setSets(initialData.sets.toString())
      setReps(initialData.reps.toString())
      setWeight(initialData.weight.toString())
    }
  }, [initialData])

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (!exercise || !sets || !reps || !weight) return

    const workoutData = {
      exercise,
      sets: parseInt(sets),
      reps: parseInt(reps),
      weight: parseFloat(weight)
    }

    if (initialData) {
      onSubmit({ ...initialData, ...workoutData })
    } else {
      onSubmit(workoutData)
    }

    // Reset form if not editing
    if (!initialData) {
      setExercise('')
      setSets('')
      setReps('')
      setWeight('')
    }
  }

  const handleCancel = () => {
    setExercise('')
    setSets('')
    setReps('')
    setWeight('')
    onCancel?.()
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div className="space-y-2">
        <Label htmlFor="exercise">Exercise</Label>
        <Popover open={open} onOpenChange={setOpen}>
          <PopoverTrigger asChild>
            <Button
              variant="outline"
              role="combobox"
              aria-expanded={open}
              className="w-full justify-between"
            >
              {exercise || "Select exercise..."}
              <ChevronsUpDown className="ml-2 h-4 w-4 shrink-0 opacity-50" />
            </Button>
          </PopoverTrigger>
          <PopoverContent className="w-full p-0">
            <Command>
              <CommandInput 
                placeholder="Search exercises..." 
                value={exercise}
                onValueChange={setExercise}
              />
              <CommandList>
                <CommandEmpty>No exercise found.</CommandEmpty>
                <CommandGroup>
                  {exerciseData
                    .filter(ex => ex.toLowerCase().includes(exercise.toLowerCase()))
                    .slice(0, 10)
                    .map((ex) => (
                      <CommandItem
                        key={ex}
                        value={ex}
                        onSelect={(currentValue) => {
                          setExercise(currentValue)
                          setOpen(false)
                        }}
                      >
                        <Check
                          className={cn(
                            "mr-2 h-4 w-4",
                            exercise === ex ? "opacity-100" : "opacity-0"
                          )}
                        />
                        {ex}
                      </CommandItem>
                    ))}
                </CommandGroup>
              </CommandList>
            </Command>
          </PopoverContent>
        </Popover>
      </div>

      <div className="grid grid-cols-3 gap-4">
        <div className="space-y-2">
          <Label htmlFor="sets">Sets</Label>
          <Input
            id="sets"
            type="number"
            value={sets}
            onChange={(e) => setSets(e.target.value)}
            placeholder="3"
            min="1"
            required
          />
        </div>
        <div className="space-y-2">
          <Label htmlFor="reps">Reps</Label>
          <Input
            id="reps"
            type="number"
            value={reps}
            onChange={(e) => setReps(e.target.value)}
            placeholder="10"
            min="1"
            required
          />
        </div>
        <div className="space-y-2">
          <Label htmlFor="weight">Weight (lbs)</Label>
          <Input
            id="weight"
            type="number"
            step="0.5"
            value={weight}
            onChange={(e) => setWeight(e.target.value)}
            placeholder="135"
            min="0"
            required
          />
        </div>
      </div>

      <div className="flex gap-2">
        <Button type="submit" className="flex-1">
          {initialData ? 'Update Exercise' : 'Add Exercise'}
        </Button>
        {initialData && (
          <Button type="button" variant="outline" onClick={handleCancel}>
            <X className="h-4 w-4" />
          </Button>
        )}
      </div>
    </form>
  )
}