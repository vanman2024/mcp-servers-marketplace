import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { GitBranch, AlertTriangle, CheckCircle, Clock, GitMerge } from 'lucide-react'

interface Branch {
  name: string
  owner: string
  lastActivity: string
  commits: number
  hasConflicts: boolean
  prStatus: 'open' | 'merged' | 'draft' | 'none'
  prNumber?: number
}

const branches: Branch[] = [
  {
    name: 'feature/user-authentication',
    owner: 'Agent-001',
    lastActivity: '2 minutes ago',
    commits: 12,
    hasConflicts: false,
    prStatus: 'open',
    prNumber: 47
  },
  {
    name: 'feature/dashboard-ui',
    owner: 'Agent-002',
    lastActivity: '5 minutes ago',
    commits: 8,
    hasConflicts: false,
    prStatus: 'draft',
    prNumber: 48
  },
  {
    name: 'fix/memory-leak',
    owner: 'Agent-003',
    lastActivity: '1 hour ago',
    commits: 3,
    hasConflicts: true,
    prStatus: 'none'
  },
  {
    name: 'feature/api-endpoints',
    owner: 'Agent-004',
    lastActivity: '15 minutes ago',
    commits: 15,
    hasConflicts: false,
    prStatus: 'open',
    prNumber: 49
  },
  {
    name: 'feature/data-visualization',
    owner: 'Agent-005',
    lastActivity: '30 minutes ago',
    commits: 22,
    hasConflicts: false,
    prStatus: 'merged',
    prNumber: 46
  },
  {
    name: 'feature/notification-system',
    owner: 'Agent-006',
    lastActivity: '45 minutes ago',
    commits: 6,
    hasConflicts: false,
    prStatus: 'none'
  },
  {
    name: 'hotfix/critical-security',
    owner: 'Agent-007',
    lastActivity: '10 minutes ago',
    commits: 2,
    hasConflicts: true,
    prStatus: 'open',
    prNumber: 50
  },
  {
    name: 'feature/mobile-responsive',
    owner: 'Agent-008',
    lastActivity: '25 minutes ago',
    commits: 9,
    hasConflicts: false,
    prStatus: 'draft',
    prNumber: 51
  }
]

const prStatusConfig = {
  open: { color: 'bg-green-500', label: 'Open' },
  draft: { color: 'bg-yellow-500', label: 'Draft' },
  merged: { color: 'bg-purple-500', label: 'Merged' },
  none: { color: 'bg-gray-500', label: 'No PR' }
}

export function BranchOverview() {
  return (
    <Card className="bg-gray-900/50 border-gray-800">
      <CardHeader>
        <CardTitle className="text-xl flex items-center space-x-2">
          <GitBranch className="w-5 h-5" />
          <span>Branch Overview</span>
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b border-gray-800">
                <th className="text-left py-3 px-4 font-medium text-gray-400">Branch</th>
                <th className="text-left py-3 px-4 font-medium text-gray-400">Owner</th>
                <th className="text-left py-3 px-4 font-medium text-gray-400">Commits</th>
                <th className="text-left py-3 px-4 font-medium text-gray-400">Status</th>
                <th className="text-left py-3 px-4 font-medium text-gray-400">PR</th>
                <th className="text-left py-3 px-4 font-medium text-gray-400">Last Activity</th>
              </tr>
            </thead>
            <tbody>
              {branches.map((branch, index) => (
                <tr key={index} className="border-b border-gray-800/50 hover:bg-gray-800/30 transition-colors">
                  <td className="py-3 px-4">
                    <div className="flex items-center space-x-2">
                      <GitBranch className="w-4 h-4 text-gray-400" />
                      <span className="font-mono text-sm">{branch.name}</span>
                    </div>
                  </td>
                  <td className="py-3 px-4">
                    <Badge variant="outline" className="text-blue-400 border-blue-400/30">
                      {branch.owner}
                    </Badge>
                  </td>
                  <td className="py-3 px-4">
                    <span className="text-sm">{branch.commits}</span>
                  </td>
                  <td className="py-3 px-4">
                    <div className="flex items-center space-x-2">
                      {branch.hasConflicts ? (
                        <div className="flex items-center space-x-1 text-red-400">
                          <AlertTriangle className="w-4 h-4" />
                          <span className="text-sm">Conflicts</span>
                        </div>
                      ) : (
                        <div className="flex items-center space-x-1 text-green-400">
                          <CheckCircle className="w-4 h-4" />
                          <span className="text-sm">Clean</span>
                        </div>
                      )}
                    </div>
                  </td>
                  <td className="py-3 px-4">
                    <div className="flex items-center space-x-2">
                      <Badge className={`${prStatusConfig[branch.prStatus].color} text-white border-0`}>
                        {prStatusConfig[branch.prStatus].label}
                      </Badge>
                      {branch.prNumber && (
                        <span className="text-xs text-gray-400">#{branch.prNumber}</span>
                      )}
                    </div>
                  </td>
                  <td className="py-3 px-4">
                    <div className="flex items-center space-x-1 text-sm text-gray-400">
                      <Clock className="w-3 h-3" />
                      <span>{branch.lastActivity}</span>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </CardContent>
    </Card>
  )
}