import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Shield, GraduationCap, Building2, Users } from 'lucide-react';

interface LoginPageProps {
  onLogin: (role: string, username: string) => void;
}

const LoginPage = ({ onLogin }: LoginPageProps) => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [role, setRole] = useState('');

  const handleLogin = (e: React.FormEvent) => {
    e.preventDefault();
    if (username && password && role) {
      onLogin(role, username);
    }
  };

  const roleIcons = {
    admin: <Shield className="h-5 w-5" />,
    faculty: <GraduationCap className="h-5 w-5" />,
    exam_center: <Building2 className="h-5 w-5" />
  };

  const roleDescriptions = {
    admin: "Full system control and key management",
    faculty: "Upload and secure exam papers",
    exam_center: "View and access exam materials"
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-background to-muted">
      <Card className="w-full max-w-md shadow-lg border-0 bg-card/95 backdrop-blur">
        <CardHeader className="text-center space-y-4">
          <div className="mx-auto w-16 h-16 bg-gradient-to-br from-primary to-accent rounded-full flex items-center justify-center shadow-lg">
            <Shield className="h-8 w-8 text-white" />
          </div>
          <div>
            <CardTitle className="text-2xl font-bold bg-gradient-to-r from-primary to-accent bg-clip-text text-transparent">
              EduSecure-HE
            </CardTitle>
            <CardDescription className="text-muted-foreground">
              Secure Exam Paper Management System
            </CardDescription>
          </div>
        </CardHeader>

        <CardContent className="space-y-6">
          <form onSubmit={handleLogin} className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="role">Role</Label>
              <Select value={role} onValueChange={setRole}>
                <SelectTrigger>
                  <SelectValue placeholder="Select your role" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="admin">
                    <div className="flex items-center gap-2">
                      {roleIcons.admin}
                      <div>
                        <div className="font-medium">Administrator</div>
                        <div className="text-xs text-muted-foreground">
                          {roleDescriptions.admin}
                        </div>
                      </div>
                    </div>
                  </SelectItem>
                  <SelectItem value="faculty">
                    <div className="flex items-center gap-2">
                      {roleIcons.faculty}
                      <div>
                        <div className="font-medium">Faculty</div>
                        <div className="text-xs text-muted-foreground">
                          {roleDescriptions.faculty}
                        </div>
                      </div>
                    </div>
                  </SelectItem>
                  <SelectItem value="exam_center">
                    <div className="flex items-center gap-2">
                      {roleIcons.exam_center}
                      <div>
                        <div className="font-medium">Exam Center</div>
                        <div className="text-xs text-muted-foreground">
                          {roleDescriptions.exam_center}
                        </div>
                      </div>
                    </div>
                  </SelectItem>
                </SelectContent>
              </Select>
            </div>

            <div className="space-y-2">
              <Label htmlFor="username">Username</Label>
              <Input
                id="username"
                type="text"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                placeholder="Enter your username"
                className="transition-all duration-200 focus:shadow-sm"
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="password">Password</Label>
              <Input
                id="password"
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="Enter your password"
                className="transition-all duration-200 focus:shadow-sm"
              />
            </div>

            <Button 
              type="submit" 
              className="w-full bg-gradient-to-r from-primary to-accent hover:from-primary-glow hover:to-accent-glow transition-all duration-300 shadow-md hover:shadow-lg"
              disabled={!username || !password || !role}
            >
              <Users className="mr-2 h-4 w-4" />
              Secure Login
            </Button>
          </form>

          <div className="text-center">
            <p className="text-xs text-muted-foreground">
              Protected by SHA-256 encryption and role-based access control
            </p>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default LoginPage;