'use client'

import { useState, useEffect } from 'react'
import { WorkoutForm } from '@/components/workout-form'
import { WorkoutList } from '@/components/workout-list'
import { WorkoutStats } from '@/components/workout-stats'
import { WorkoutHistory } from '@/components/workout-history'
import { ThemeToggle } from '@/components/theme-toggle'
import { useLocalStorage } from '@/hooks/use-local-storage'
import { Workout } from '@/lib/types'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Dumbbell } from 'lucide-react'

export default function Home() {
  const [workouts, setWorkouts] = useLocalStorage<Workout[]>('workouts', [])
  const [editingWorkout, setEditingWorkout] = useState<Workout | null>(null)

  const addWorkout = (workout: Omit<Workout, 'id' | 'date'>) => {
    const newWorkout: Workout = {
      ...workout,
      id: Date.now().toString(),
      date: new Date().toISOString().split('T')[0]
    }
    setWorkouts([...workouts, newWorkout])
  }

  const updateWorkout = (updatedWorkout: Workout) => {
    setWorkouts(workouts.map(w => w.id === updatedWorkout.id ? updatedWorkout : w))
    setEditingWorkout(null)
  }

  const deleteWorkout = (id: string) => {
    setWorkouts(workouts.filter(w => w.id !== id))
  }

  const todaysWorkouts = workouts.filter(w => w.date === new Date().toISOString().split('T')[0])

  return (
    <div className="min-h-screen bg-background">
      <div className="container mx-auto px-4 py-8 max-w-6xl">
        <header className="flex items-center justify-between mb-8">
          <div className="flex items-center gap-3">
            <Dumbbell className="h-8 w-8 text-primary" />
            <h1 className="text-3xl font-bold">Workout Tracker</h1>
          </div>
          <ThemeToggle />
        </header>

        <Tabs defaultValue="today" className="space-y-6">
          <TabsList className="grid w-full grid-cols-3">
            <TabsTrigger value="today">Today's Workout</TabsTrigger>
            <TabsTrigger value="history">History</TabsTrigger>
            <TabsTrigger value="stats">Statistics</TabsTrigger>
          </TabsList>

          <TabsContent value="today" className="space-y-6">
            <div className="grid gap-6 lg:grid-cols-2">
              <Card>
                <CardHeader>
                  <CardTitle>
                    {editingWorkout ? 'Edit Exercise' : 'Add New Exercise'}
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <WorkoutForm
                    onSubmit={editingWorkout ? updateWorkout : addWorkout}
                    initialData={editingWorkout}
                    onCancel={() => setEditingWorkout(null)}
                  />
                </CardContent>
              </Card>

              <WorkoutStats workouts={todaysWorkouts} />
            </div>

            <WorkoutList
              workouts={todaysWorkouts}
              onEdit={setEditingWorkout}
              onDelete={deleteWorkout}
            />
          </TabsContent>

          <TabsContent value="history">
            <WorkoutHistory workouts={workouts} />
          </TabsContent>

          <TabsContent value="stats">
            <WorkoutStats workouts={workouts} showAllTime />
          </TabsContent>
        </Tabs>
      </div>
    </div>
  )
}