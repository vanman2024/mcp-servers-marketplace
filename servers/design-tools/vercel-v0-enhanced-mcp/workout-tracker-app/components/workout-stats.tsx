'use client'

import { Workout } from '@/lib/types'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Activity, Target, TrendingUp, Calendar } from 'lucide-react'

interface WorkoutStatsProps {
  workouts: Workout[]
  showAllTime?: boolean
}

export function WorkoutStats({ workouts, showAllTime = false }: WorkoutStatsProps) {
  const totalExercises = workouts.length
  const totalSets = workouts.reduce((sum, w) => sum + w.sets, 0)
  const totalVolume = workouts.reduce((sum, w) => sum + (w.sets * w.reps * w.weight), 0)
  const uniqueExercises = new Set(workouts.map(w => w.exercise)).size

  const stats = [
    {
      title: showAllTime ? 'Total Exercises' : 'Exercises Today',