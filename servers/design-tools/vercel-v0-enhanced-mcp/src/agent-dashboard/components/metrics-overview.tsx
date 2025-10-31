import { Card, CardContent } from '@/components/ui/card'
import { Activity, HardDrive, GitPullRequest, CheckCircle } from 'lucide-react'

const metrics = [
  {
    title: 'Active Agents',
    value: '8',
    change: '+2',
    icon: Activity,
    color: 'text-green-400',
    bgColor: 'bg-green-400/10'
  },
  {
    title: 'Disk Usage',
    value: '2.4 GB',
    change: '+120 MB',
    icon: HardDrive,
    color: 'text-blue-400',
    bgColor: 'bg-blue-400/10'
  },
  {
    title: 'Pending PRs',
    value: '12',
    change: '+3',
    icon: GitPullRequest,
    color: 'text-yellow-400',
    bgColor: 'bg-yellow-400/10'
  },
  {
    title: 'Tasks Completed',
    value: '47',
    change: '+15',
    icon: CheckCircle,
    color: 'text-purple-400',
    bgColor: 'bg-purple-400/10'
  }
]

export function MetricsOverview() {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
      {metrics.map((metric, index) => (
        <Card key={index} className="bg-gray-900/50 border-gray-800 hover:bg-gray-900/70 transition-colors">
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-400">{metric.title}</p>
                <div className="flex items-center space-x-2 mt-2">
                  <p className="text-2xl font-bold">{metric.value}</p>
                  <span className={`text-xs px-2 py-1 rounded-full ${metric.bgColor} ${metric.color}`}>
                    {metric.change}
                  </span>
                </div>
              </div>
              <div className={`p-3 rounded-lg ${metric.bgColor}`}>
                <metric.icon className={`w-6 h-6 ${metric.color}`} />
              </div>
            </div>
          </CardContent>
        </Card>
      ))}
    </div>
  )
}