import { ProgressCharts } from '@/components/progress-charts'

export default function ProgressPage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Progress</h1>
        <p className="text-muted-foreground">
          Visualize your strength gains and workout consistency
        </p>
      </div>
      <ProgressCharts />
    </div>
  )
}