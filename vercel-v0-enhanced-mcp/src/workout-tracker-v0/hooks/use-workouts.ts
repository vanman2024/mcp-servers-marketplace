'use client'

import { useState, useEffect } from 'react'
import type { Workout } from '@/types/workout'

const STORAGE_KEY = 'workout-tracker-data'

export function useWorkouts() {
  const [workouts, setWorkouts] = useState<Workout[]>([])

  // Load workouts from localStorage on mount
  useEffect(() => {
    try {
      const stored = localStorage.getItem(STORAGE_KEY)
      if (stored) {
        const parsedWorkouts = JSON.parse(stored)
        setWorkouts(parsedWorkouts.sort((a: Workout, b: Workout) => 
          new Date(b.date).getTime() - new Date(a.date).getTime()
        ))
      }
    } catch (error) {
      console.error('Failed to load workouts from localStorage:', error)
    }
  }, [])

  // Save workouts to localStorage whenever workouts change
  useEffect(() => {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(workouts))
    } catch (error) {
      console.error('Failed to save workouts to localStorage:', error)
    }
  }, [workouts])

  const addWorkout = (workout: Workout) => {
    setWorkouts(prev => {
      const updated = [workout, ...prev]
      return updated.sort((a, b) => 
        new Date(b.date).getTime() - new Date(a.date).getTime()
      )
    })
  }

  const removeWorkout = (index: number) => {
    setWorkouts(prev => prev.filter((_, i) => i !== index))
  }

  const updateWorkout = (index: number, updatedWorkout: Workout) => {
    setWorkouts(prev => {
      const updated = [...prev]
      updated[index] = updatedWorkout
      return updated.sort((a, b) => 
        new Date(b.date).getTime() - new Date(a.date).getTime()
      )
    })
  }

  const getWorkoutsByExercise = (exerciseName: string) => {
    return workouts.filter(workout => 
      workout.exercises.some(exercise => 
        exercise.name.toLowerCase() === exerciseName.toLowerCase()
      )
    )
  }

  const getExerciseHistory = (exerciseName: string) => {
    const exerciseWorkouts = getWorkoutsByExercise(exerciseName)
    return exerciseWorkouts.map(workout => {
      const exercise = workout.exercises.find(ex => 
        ex.name.toLowerCase() === exerciseName.toLowerCase()
      )
      return {
        date: workout.date,
        exercise: exercise!
      }
    }).sort((a, b) => new Date(a.date).getTime() - new Date(b.date).getTime())
  }

  const getAllExerciseNames = () => {
    const exerciseNames = new Set<string>()
    workouts.forEach(workout => {
      workout.exercises.forEach(exercise => {
        exerciseNames.add(exercise.name)
      })
    })
    return Array.from(exerciseNames).sort()
  }

  return {
    workouts,
    addWorkout,
    removeWorkout,
    updateWorkout,
    getWorkoutsByExercise,
    getExerciseHistory,
    getAllExerciseNames
  }
}