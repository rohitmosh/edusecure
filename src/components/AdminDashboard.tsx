import { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { useToast } from '@/hooks/use-toast';
import { 
  Shield, 
  Key, 
  FileCheck, 
  Clock, 
  AlertTriangle, 
  Eye, 
  Calendar,
  Activity,
  Lock,
  Unlock,
  CheckCircle,
  Loader2,
  Trash2,
  RefreshCw
} from 'lucide-react';

interface AdminDashboardProps {
  username: string;
  onLogout: () => void;
}

const AdminDashboard = ({ username, onLogout }: AdminDashboardProps) => {
  const [examPapers, setExamPapers] = useState<any[]>([]);
  const [systemLogs, setSystemLogs] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [keyReleasing, setKeyReleasing] = useState<string | null>(null);
  const [deleting, setDeleting] = useState<string | null>(null);
  const { toast } = useToast();

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      setLoading(true);
      
      // Fetch exam papers
      const papersResponse = await fetch('http://localhost:5000/api/admin/papers', {
        credentials: 'include'
      });
      
      if (papersResponse.ok) {
        const papersData = await papersResponse.json();
        setExamPapers(papersData.papers || []);
      }

      // Fetch logs
      const logsResponse = await fetch('http://localhost:5000/api/admin/logs', {
        credentials: 'include'
      });
      
      if (logsResponse.ok) {
        const logsData = await logsResponse.json();
        setSystemLogs(logsData.logs || []);
      }
      
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to fetch dashboard data",
        variant: "destructive"
      });
    } finally {
      setLoading(false);
    }
  };

  const handleReleaseKey = async (examId: string) => {
    try {
      setKeyReleasing(examId);
      
      const response = await fetch(`http://localhost:5000/api/admin/release_key/${examId}`, {
        method: 'POST',
        credentials: 'include'
      });

      const data = await response.json();

      if (response.ok) {
        toast({
          title: "Key Released",
          description: `Chaos key for exam ${examId} has been released successfully.`
        });
        fetchData(); // Refresh data
      } else {
        toast({
          title: "Release Failed",
          description: data.error || 'Failed to release key',
          variant: "destructive"
        });
      }
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to release key",
        variant: "destructive"
      });
    } finally {
      setKeyReleasing(null);
    }
  };

  const handleVerifyIntegrity = async (examId: string) => {
    try {
      const response = await fetch(`http://localhost:5000/api/admin/verify_integrity/${examId}`, {
        credentials: 'include'
      });

      const data = await response.json();

      if (response.ok) {
        const isValid = data.valid;
        toast({
          title: isValid ? "Integrity Verified" : "Integrity Failed",
          description: isValid 
            ? `All ${data.total_pages} pages are intact and unmodified.`
            : "Some files have been tampered with!",
          variant: isValid ? "default" : "destructive"
        });
      } else {
        toast({
          title: "Verification Failed",
          description: data.error || 'Failed to verify integrity',
          variant: "destructive"
        });
      }
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to verify integrity",
        variant: "destructive"
      });
    }
  };

  const handleDeletePaper = async (examId: string) => {
    try {
      // Confirm deletion
      if (!window.confirm(`Are you sure you want to delete exam paper "${examId}"? This action cannot be undone.`)) {
        return;
      }

      setDeleting(examId);
      
      const response = await fetch(`http://localhost:5000/api/admin/delete_paper/${examId}`, {
        method: 'DELETE',
        credentials: 'include'
      });

      const data = await response.json();

      if (response.ok) {
        toast({
          title: "Paper Deleted",
          description: `Exam paper ${examId} has been permanently deleted.`
        });
        fetchData(); // Refresh data
      } else {
        toast({
          title: "Deletion Failed",
          description: data.error || 'Failed to delete paper',
          variant: "destructive"
        });
      }
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to delete paper",
        variant: "destructive"
      });
    } finally {
      setDeleting(null);
    }
  };

  return (
    <div className="min-h-screen bg-background p-6">
      <div className="max-w-7xl mx-auto space-y-6">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-4">
            <div className="w-12 h-12 bg-gradient-to-br from-primary to-accent rounded-full flex items-center justify-center">
              <Shield className="h-6 w-6 text-white" />
            </div>
            <div>
              <h1 className="text-3xl font-bold text-foreground">Admin Dashboard</h1>
              <p className="text-muted-foreground">Welcome, {username}</p>
            </div>
          </div>
          <div className="flex items-center gap-2">
            <Button variant="outline" size="sm" onClick={fetchData} disabled={loading}>
              {loading ? (
                <Loader2 className="h-4 w-4 mr-1 animate-spin" />
              ) : (
                <RefreshCw className="h-4 w-4 mr-1" />
              )}
              Refresh
            </Button>
            <Button variant="outline" onClick={onLogout}>
              Logout
            </Button>
          </div>
        </div>

        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <Card className="border-0 shadow-md bg-gradient-to-br from-primary/10 to-primary/5">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-muted-foreground">Total Papers</p>
                  <p className="text-2xl font-bold text-foreground">{examPapers.length}</p>
                </div>
                <FileCheck className="h-8 w-8 text-primary" />
              </div>
            </CardContent>
          </Card>

          <Card className="border-0 shadow-md bg-gradient-to-br from-accent/10 to-accent/5">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-muted-foreground">Released Keys</p>
                  <p className="text-2xl font-bold text-foreground">
                    {examPapers.filter(exam => exam.key_released).length}
                  </p>
                </div>
                <Key className="h-8 w-8 text-accent" />
              </div>
            </CardContent>
          </Card>

          <Card className="border-0 shadow-md bg-gradient-to-br from-warning/10 to-warning/5">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-muted-foreground">Pending Release</p>
                  <p className="text-2xl font-bold text-foreground">
                    {examPapers.filter(exam => !exam.key_released).length}
                  </p>
                </div>
                <Clock className="h-8 w-8 text-warning" />
              </div>
            </CardContent>
          </Card>

          <Card className="border-0 shadow-md bg-gradient-to-br from-destructive/10 to-destructive/5">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-muted-foreground">Log Entries</p>
                  <p className="text-2xl font-bold text-foreground">{systemLogs.length}</p>
                </div>
                <Activity className="h-8 w-8 text-destructive" />
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Main Content */}
        <Tabs defaultValue="papers" className="space-y-6">
          <TabsList className="grid w-full grid-cols-3">
            <TabsTrigger value="papers">Exam Papers</TabsTrigger>
            <TabsTrigger value="keys">Key Management</TabsTrigger>
            <TabsTrigger value="logs">Security Logs</TabsTrigger>
          </TabsList>

          <TabsContent value="papers" className="space-y-4">
            <Card className="border-0 shadow-md">
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <FileCheck className="h-5 w-5" />
                  Exam Papers Overview
                </CardTitle>
                <CardDescription>
                  Monitor and manage all uploaded exam papers
                </CardDescription>
              </CardHeader>
              <CardContent>
                {loading ? (
                  <div className="flex items-center justify-center p-8">
                    <Loader2 className="h-8 w-8 animate-spin" />
                  </div>
                ) : examPapers.length === 0 ? (
                  <div className="text-center p-8 text-muted-foreground">
                    No exam papers uploaded yet
                  </div>
                ) : (
                  <div className="space-y-4">
                    {examPapers.map((exam) => (
                      <div key={exam.exam_id} className="flex items-center justify-between p-4 border border-border rounded-lg bg-card/50">
                        <div className="flex-1">
                          <h3 className="font-semibold text-foreground">{exam.exam_id}</h3>
                          <div className="flex items-center gap-4 mt-2 text-sm text-muted-foreground">
                            <span>Uploaded by: {exam.uploader}</span>
                            <span>Pages: {exam.total_pages}</span>
                            <span>Upload Time: {new Date(exam.upload_time).toLocaleString()}</span>
                          </div>
                          <div className="flex items-center gap-2 mt-2">
                            <Badge variant={exam.key_released ? 'default' : 'secondary'}>
                              {exam.key_released ? 'Key Released' : 'Pending'}
                            </Badge>
                            <Badge variant="default">
                              <CheckCircle className="h-3 w-3 mr-1" />
                              Encrypted
                            </Badge>
                          </div>
                        </div>
                        <div className="flex items-center gap-2">
                          <Button variant="outline" size="sm" onClick={() => handleVerifyIntegrity(exam.exam_id)}>
                            <Eye className="h-4 w-4 mr-1" />
                            Verify
                          </Button>
                          <Button variant="outline" size="sm">
                            <Calendar className="h-4 w-4 mr-1" />
                            {new Date(exam.scheduled_time).toLocaleString()}
                          </Button>
                          <Button 
                            variant="destructive" 
                            size="sm" 
                            onClick={() => handleDeletePaper(exam.exam_id)}
                            disabled={deleting === exam.exam_id}
                          >
                            {deleting === exam.exam_id ? (
                              <Loader2 className="h-4 w-4 mr-1 animate-spin" />
                            ) : (
                              <Trash2 className="h-4 w-4 mr-1" />
                            )}
                            Delete
                          </Button>
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="keys" className="space-y-4">
            <Card className="border-0 shadow-md">
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Key className="h-5 w-5" />
                  Chaos Key Management
                </CardTitle>
                <CardDescription>
                  Control the release of decryption keys for scheduled exams
                </CardDescription>
              </CardHeader>
              <CardContent>
                {loading ? (
                  <div className="flex items-center justify-center p-8">
                    <Loader2 className="h-8 w-8 animate-spin" />
                  </div>
                ) : examPapers.length === 0 ? (
                  <div className="text-center p-8 text-muted-foreground">
                    No exam papers available for key management
                  </div>
                ) : (
                  <div className="space-y-4">
                    {examPapers.map((exam) => (
                      <div key={exam.exam_id} className="flex items-center justify-between p-4 border border-border rounded-lg bg-card/50">
                        <div className="flex-1">
                          <h3 className="font-semibold text-foreground">{exam.exam_id}</h3>
                          <p className="text-sm text-muted-foreground">
                            Scheduled: {new Date(exam.scheduled_time).toLocaleString()}
                          </p>
                        </div>
                        <div className="flex items-center gap-2">
                          {!exam.key_released ? (
                            <Button 
                              onClick={() => handleReleaseKey(exam.exam_id)}
                              disabled={keyReleasing === exam.exam_id}
                              className="bg-gradient-to-r from-accent to-accent-glow"
                            >
                              {keyReleasing === exam.exam_id ? (
                                <Loader2 className="h-4 w-4 mr-1 animate-spin" />
                              ) : (
                                <Unlock className="h-4 w-4 mr-1" />
                              )}
                              Release Key
                            </Button>
                          ) : (
                            <Button variant="outline" disabled>
                              <CheckCircle className="h-4 w-4 mr-1" />
                              Key Released
                            </Button>
                          )}
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="logs" className="space-y-4">
            <Card className="border-0 shadow-md">
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Activity className="h-5 w-5" />
                  Security Audit Logs
                </CardTitle>
                <CardDescription>
                  Tamper-proof hash-chained activity logs
                </CardDescription>
              </CardHeader>
              <CardContent>
                {loading ? (
                  <div className="flex items-center justify-center p-8">
                    <Loader2 className="h-8 w-8 animate-spin" />
                  </div>
                ) : systemLogs.length === 0 ? (
                  <div className="text-center p-8 text-muted-foreground">
                    No system logs available
                  </div>
                ) : (
                  <div className="space-y-2 max-h-96 overflow-y-auto">
                    {systemLogs.slice(-20).reverse().map((log) => {
                      const getEventColor = (event: string) => {
                        switch (event) {
                          case 'login': return 'bg-blue-500';
                          case 'logout': return 'bg-gray-500';
                          case 'upload': return 'bg-green-500';
                          case 'download': return 'bg-yellow-500';
                          case 'delete_paper': return 'bg-red-500';
                          case 'delete_paper_failed': return 'bg-red-700';
                          case 'key_release': return 'bg-purple-500';
                          case 'verify': return 'bg-cyan-500';
                          case 'decrypt': return 'bg-orange-500';
                          default: return 'bg-accent';
                        }
                      };

                      const getEventIcon = (event: string) => {
                        switch (event) {
                          case 'delete_paper': return '🗑️';
                          case 'delete_paper_failed': return '❌';
                          case 'upload': return '📤';
                          case 'download': return '📥';
                          case 'login': return '🔐';
                          case 'logout': return '🚪';
                          case 'key_release': return '🔑';
                          case 'verify': return '✅';
                          case 'decrypt': return '🔓';
                          default: return '📋';
                        }
                      };

                      return (
                        <div key={log.id} className="flex items-start justify-between p-4 border border-border rounded-lg bg-card/30 hover:bg-card/50 transition-colors">
                          <div className="flex items-start gap-4 flex-1">
                            <div className={`w-3 h-3 rounded-full ${getEventColor(log.event)} mt-1 flex-shrink-0`}></div>
                            <div className="flex-1 min-w-0">
                              <div className="flex items-center gap-2 mb-1">
                                <span className="text-lg">{getEventIcon(log.event)}</span>
                                <span className="font-medium text-foreground capitalize">{log.event.replace('_', ' ')}</span>
                                <Badge variant="outline" className="text-xs">
                                  ID: {log.id}
                                </Badge>
                              </div>
                              <div className="text-sm text-muted-foreground">
                                <span className="font-medium">User:</span> {log.user}
                                {log.exam_id && (
                                  <>
                                    <span className="mx-2">•</span>
                                    <span className="font-medium">Exam:</span> {log.exam_id}
                                  </>
                                )}
                              </div>
                              {log.details && (
                                <div className="text-sm text-muted-foreground mt-1 break-words">
                                  {log.details}
                                </div>
                              )}
                            </div>
                          </div>
                          <div className="flex flex-col items-end gap-1 ml-4 flex-shrink-0">
                            <span className="text-xs text-muted-foreground">
                              {new Date(log.timestamp).toLocaleDateString()}
                            </span>
                            <span className="text-xs text-muted-foreground">
                              {new Date(log.timestamp).toLocaleTimeString()}
                            </span>
                            <Badge 
                              variant={log.event.includes('failed') || log.event.includes('error') ? 'destructive' : 'default'}
                              className="text-xs"
                            >
                              {log.event}
                            </Badge>
                          </div>
                        </div>
                      );
                    })}
                  </div>
                )}
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </div>
    </div>
  );
};

export default AdminDashboard;