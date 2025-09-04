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
  Loader2
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
          <Button variant="outline" onClick={onLogout}>
            Logout
          </Button>
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
                  <div className="space-y-2">
                    {systemLogs.slice(-10).reverse().map((log) => (
                      <div key={log.id} className="flex items-center justify-between p-3 border border-border rounded-lg bg-card/30">
                        <div className="flex items-center gap-4">
                          <div className="w-2 h-2 rounded-full bg-accent"></div>
                          <div>
                            <span className="font-medium text-foreground">{log.event}</span>
                            <span className="text-muted-foreground ml-2">by {log.user}</span>
                            {log.exam_id && (
                              <span className="text-muted-foreground ml-2">on {log.exam_id}</span>
                            )}
                          </div>
                        </div>
                        <div className="flex items-center gap-2">
                          <span className="text-sm text-muted-foreground">
                            {new Date(log.timestamp).toLocaleTimeString()}
                          </span>
                          <Badge variant="default">
                            {log.event}
                          </Badge>
                        </div>
                      </div>
                    ))}
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