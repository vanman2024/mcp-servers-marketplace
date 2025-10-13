'use client'

import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { useWorkouts } from '@/hooks/use-workouts'
import { useMemo } from 'react'
import { TrendingUp, Calendar, BarChart3 } from 'lucide-react'

export function ProgressCharts() {
  const { workouts } = useWorkouts()

  const chartData = useMemo(() => {
    const exerciseProgress: Record<string, Array<{ date: string; maxWeight: number }>> = {}
    
    workouts.forEach(workout => {
      workout.exercises.forEach(exercise => {
        if (!exerciseProgress[exercise.name]) {
          exerciseProgress[exercise.name] = []
        }
        
        const maxWeight = Math.max(...exercise.sets.map(set => set.weight))
        exerciseProgress[exercise.name].push({
          date: workout.date,
          maxWeight
        })
      })
    })

    // Sort by date and get recent progress
    Object.keys(exerciseProgress).forEach(exerciseName => {
      exerciseProgress[exerciseName].sort((a, b) => 
        new Date(a.date).getTime() - new Date(b.date).getTime()
      )
    })

    return exerciseProgress
  }, [workouts])

  const weeklyWorkouts = useMemo(() => {
    const weeks: Record<string, number> = {}
    
    workouts.forEach(workout => {
      const date = new Date(workout.date)
      const weekStart = new Date(date)
      weekStart.setDate(date.getDate() - date.getDay())
      const weekKey = weekStart.toISOString().split('T')[0]
      
      weeks[weekKey] = (weeks[weekKey] || 0) + 1
    })

    return Object.entries(weeks)
      .sort(([a], [b]) => a.localeCompare(b))
      .slice(-8) // Last 8 weeks
  }, [workouts])

  if (workouts.length === 0) {
    return (
      <Card>
        <CardContent className="py-12">
          <div className="text-center">
            <BarChart3 className="h-16 w-16 mx-auto text-muted-foreground mb-4" />
            <h3 className="text-lg font-semibold mb-2">No progress data yet</h3>
            <p className="text-muted-foreground">
              Complete a few workouts to see your progress charts.
            </p>
          </div>
        </CardContent>
      </Card>
    )
  }

  return (
    <div className="space-y-6">
      {/* Weekly Workout Frequency */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <Calendar className="h-5 w-5" />
            <span>Weekly Workout Frequency</span>
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-3">
            {weeklyWorkouts.map(([week, count]) => (
              <div key={week} className="flex items-center space-x-3">
                <span className="text-sm text-muted-foreground w-24">
                  {new Date(week).toLocaleDateString('en-US', { 
                    month: 'short', 
                    day: 'numeric' 
                  })}
                </span>
                <div className="flex-1 bg-secondary rounded-full h-6 relative">
                  <div 
                    className="bg-primary rounded-full h-6 flex items-center justify-end pr-2"
                    style={{ width: `${Math.min((count / 7) * 100, 100)}%` }}
                  >
                    <span className="text-xs text-primary-foreground font-medium">
                      {count}
                    </span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Exercise Progress */}
      {Object.entries(chartData).map(([exerciseName, progress]) => {
        if (progress.length < 2) return null
        
        const latestWeight = progress[progress.length - 1].maxWeight
        const previousWeight = progress[progress.length - 2].maxWeight
        const improvement = latestWeight - previousWeight
        const improvementPercent = previousWeight > 0 ? (improvement / previousWeight) * 100 : 0

        return (
          <Card key={exerciseName}>
            <CardHeader>
              <CardTitle className="flex items-center justify-between">
                <div className="flex items-center space-x-2">
                  <TrendingUp className="h-5 w-5" />
                  <span>{exerciseName}</span>
                </div>
                <div className="text-right">
                  <div className="text-sm text-muted-foreground">Latest Max</div>
                  <div className="font-bold">{latestWeight} lbs</div>
                  {improvement !== 0 && (
                    <div className={`text-xs ${improvement > 0 ? 'text-green-600' : 'text-red-600'}`}>
                      {improvement > 0 ? '+' : ''}{improvement} lbs ({improvementPercent.toFixed(1)}%)
                    </div>
                  )}
                </div>
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-2">
                {progress.slice(-5).map((entry, index) => {
                  const maxWeight = Math.max(...progress.map(p => p.maxWeight))
                  const percentage = (entry.maxWeight / maxWeight) * 100
                  
                  return (
                    <div key={index} className="flex items-center space-x-3">
                      <span className="text-sm text-muted-foreground w-20">
                        {new Date(entry.date).toLocaleDateString('en-US', { 
                          month: 'short', 
                          day: 'numeric' 
                        })}
                      </span>
                      <div className="flex-1 bg-secondary rounded-full h-6 relative">
                        <div 
                          className="bg-primary rounded-full h-6 flex items-center justify-end pr-2"
                          style={{ width: `${percentage}%` }}
                        >
                          <span className="text-xs text-primary-foreground font-medium">
                            {entry.maxWeight}
                          </span>
                        </div>
                      </div>
                    </div>
                  )
                })}
              </div>
            </CardContent>
          </Card>
        )
      })}
    </div>
  )
}