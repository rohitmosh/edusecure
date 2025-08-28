import { useState, useRef } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import { Progress } from '@/components/ui/progress';
import { 
  Upload, 
  FileText, 
  Shield, 
  Eye, 
  EyeOff, 
  CheckCircle, 
  AlertCircle,
  Hash,
  Key,
  Clock
} from 'lucide-react';
import { useToast } from '@/hooks/use-toast';

interface FacultyUploadProps {
  username: string;
  onLogout: () => void;
}

const FacultyUpload = ({ username, onLogout }: FacultyUploadProps) => {
  const [file, setFile] = useState<File | null>(null);
  const [examTitle, setExamTitle] = useState('');
  const [description, setDescription] = useState('');
  const [isProcessing, setIsProcessing] = useState(false);
  const [processingStep, setProcessingStep] = useState('');
  const [progress, setProgress] = useState(0);
  const [showOriginal, setShowOriginal] = useState(true);
  const [isUploaded, setIsUploaded] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const { toast } = useToast();

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = e.target.files?.[0];
    if (selectedFile) {
      if (selectedFile.type === 'application/pdf' || selectedFile.name.endsWith('.docx')) {
        setFile(selectedFile);
        setIsUploaded(false);
      } else {
        toast({
          title: "Invalid File Type",
          description: "Please select a PDF or DOCX file.",
          variant: "destructive"
        });
      }
    }
  };

  const simulateProcessing = async () => {
    setIsProcessing(true);
    setProgress(0);

    const steps = [
      { step: 'Converting PDF to images...', duration: 1500 },
      { step: 'Applying chaotic pixel scrambling...', duration: 2000 },
      { step: 'Computing SHA-256 hash...', duration: 1000 },
      { step: 'Encrypting metadata with Paillier...', duration: 1500 },
      { step: 'Generating chaos key...', duration: 1000 },
      { step: 'Finalizing secure upload...', duration: 1000 }
    ];

    for (let i = 0; i < steps.length; i++) {
      setProcessingStep(steps[i].step);
      setProgress((i + 1) * (100 / steps.length));
      await new Promise(resolve => setTimeout(resolve, steps[i].duration));
    }

    setIsProcessing(false);
    setIsUploaded(true);
    setShowOriginal(false);
    
    toast({
      title: "Upload Successful",
      description: "Exam paper has been securely scrambled and uploaded.",
    });
  };

  const handleUpload = async () => {
    if (!file || !examTitle) {
      toast({
        title: "Missing Information",
        description: "Please provide both a file and exam title.",
        variant: "destructive"
      });
      return;
    }

    await simulateProcessing();
  };

  return (
    <div className="min-h-screen bg-background p-6">
      <div className="max-w-4xl mx-auto space-y-6">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-4">
            <div className="w-12 h-12 bg-gradient-to-br from-primary to-accent rounded-full flex items-center justify-center">
              <Upload className="h-6 w-6 text-white" />
            </div>
            <div>
              <h1 className="text-3xl font-bold text-foreground">Faculty Upload</h1>
              <p className="text-muted-foreground">Welcome, {username}</p>
            </div>
          </div>
          <Button variant="outline" onClick={onLogout}>
            Logout
          </Button>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Upload Form */}
          <Card className="border-0 shadow-lg">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <FileText className="h-5 w-5" />
                Upload Exam Paper
              </CardTitle>
              <CardDescription>
                Securely upload and encrypt exam papers with chaotic scrambling
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="space-y-2">
                <Label htmlFor="examTitle">Exam Title</Label>
                <Input
                  id="examTitle"
                  value={examTitle}
                  onChange={(e) => setExamTitle(e.target.value)}
                  placeholder="e.g., Advanced Mathematics Final Exam"
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="description">Description (Optional)</Label>
                <Textarea
                  id="description"
                  value={description}
                  onChange={(e) => setDescription(e.target.value)}
                  placeholder="Additional details about the exam..."
                  rows={3}
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="file">Exam Paper File</Label>
                <div className="flex items-center gap-2">
                  <Input
                    ref={fileInputRef}
                    id="file"
                    type="file"
                    accept=".pdf,.docx"
                    onChange={handleFileSelect}
                    className="hidden"
                  />
                  <Button
                    variant="outline"
                    onClick={() => fileInputRef.current?.click()}
                    className="w-full"
                  >
                    <Upload className="h-4 w-4 mr-2" />
                    {file ? file.name : 'Select PDF or DOCX file'}
                  </Button>
                </div>
              </div>

              {isProcessing && (
                <div className="space-y-3">
                  <div className="flex items-center gap-2 text-sm text-muted-foreground">
                    <div className="w-4 h-4 border-2 border-primary border-t-transparent rounded-full animate-spin"></div>
                    {processingStep}
                  </div>
                  <Progress value={progress} className="w-full" />
                </div>
              )}

              <Button
                onClick={handleUpload}
                disabled={!file || !examTitle || isProcessing}
                className="w-full bg-gradient-to-r from-primary to-accent hover:from-primary-glow hover:to-accent-glow"
              >
                {isProcessing ? 'Processing...' : 'Secure Upload'}
              </Button>

              {isUploaded && (
                <div className="flex items-center gap-2 p-3 bg-accent/10 border border-accent/20 rounded-lg">
                  <CheckCircle className="h-5 w-5 text-accent" />
                  <div>
                    <p className="font-medium text-accent">Upload Complete</p>
                    <p className="text-sm text-muted-foreground">
                      Paper encrypted and stored securely
                    </p>
                  </div>
                </div>
              )}
            </CardContent>
          </Card>

          {/* Preview */}
          <Card className="border-0 shadow-lg">
            <CardHeader>
              <CardTitle className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <Shield className="h-5 w-5" />
                  Security Preview
                </div>
                {file && (
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() => setShowOriginal(!showOriginal)}
                  >
                    {showOriginal ? <EyeOff className="h-4 w-4 mr-1" /> : <Eye className="h-4 w-4 mr-1" />}
                    {showOriginal ? 'Hide' : 'Show'} Original
                  </Button>
                )}
              </CardTitle>
              <CardDescription>
                Visual representation of the scrambling process
              </CardDescription>
            </CardHeader>
            <CardContent>
              {!file ? (
                <div className="flex flex-col items-center justify-center h-64 border-2 border-dashed border-border rounded-lg bg-muted/20">
                  <FileText className="h-12 w-12 text-muted-foreground mb-4" />
                  <p className="text-muted-foreground">Select a file to see preview</p>
                </div>
              ) : (
                <div className="space-y-4">
                  <div className="grid grid-cols-2 gap-4">
                    <div className="space-y-2">
                      <Label className="text-sm font-medium">Original Paper</Label>
                      <div className={`aspect-[3/4] bg-gradient-to-br from-gray-100 to-gray-200 rounded-lg flex items-center justify-center transition-all duration-300 ${showOriginal ? 'opacity-100' : 'opacity-30 blur-sm'}`}>
                        <div className="text-center p-4">
                          <FileText className="h-8 w-8 mx-auto mb-2 text-gray-600" />
                          <p className="text-xs text-gray-600">Readable Content</p>
                          <div className="mt-2 space-y-1">
                            <div className="h-1 bg-gray-400 rounded w-3/4 mx-auto"></div>
                            <div className="h-1 bg-gray-400 rounded w-full mx-auto"></div>
                            <div className="h-1 bg-gray-400 rounded w-2/3 mx-auto"></div>
                          </div>
                        </div>
                      </div>
                    </div>

                    <div className="space-y-2">
                      <Label className="text-sm font-medium">Scrambled Paper</Label>
                      <div className="aspect-[3/4] bg-gradient-to-br from-red-100 to-red-200 rounded-lg flex items-center justify-center">
                        <div className="text-center p-2">
                          <AlertCircle className="h-8 w-8 mx-auto mb-2 text-red-600" />
                          <p className="text-xs text-red-600">Unreadable</p>
                          <div className="mt-2 grid grid-cols-4 gap-1">
                            {Array.from({ length: 16 }).map((_, i) => (
                              <div key={i} className="h-1 bg-red-400 rounded" style={{
                                transform: `rotate(${Math.random() * 360}deg)`,
                              }}></div>
                            ))}
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>

                  {isUploaded && (
                    <div className="space-y-3 mt-6">
                      <div className="flex items-center gap-2 p-3 bg-muted/30 rounded-lg">
                        <Hash className="h-4 w-4 text-primary" />
                        <div className="flex-1">
                          <p className="text-sm font-medium">SHA-256 Hash Generated</p>
                          <p className="text-xs text-muted-foreground font-mono">
                            a1b2c3d4e5f6...
                          </p>
                        </div>
                      </div>
                      
                      <div className="flex items-center gap-2 p-3 bg-muted/30 rounded-lg">
                        <Key className="h-4 w-4 text-accent" />
                        <div className="flex-1">
                          <p className="text-sm font-medium">Chaos Key Encrypted</p>
                          <p className="text-xs text-muted-foreground">
                            Secured for Admin release only
                          </p>
                        </div>
                      </div>

                      <div className="flex items-center gap-2 p-3 bg-muted/30 rounded-lg">
                        <Clock className="h-4 w-4 text-warning" />
                        <div className="flex-1">
                          <p className="text-sm font-medium">Pending Schedule</p>
                          <p className="text-xs text-muted-foreground">
                            Awaiting Admin time-lock setup
                          </p>
                        </div>
                      </div>
                    </div>
                  )}
                </div>
              )}
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
};

export default FacultyUpload;