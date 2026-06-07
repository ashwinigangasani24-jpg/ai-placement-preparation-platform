import { BrowserRouter as Router, Routes, Route, useNavigate, useLocation } from 'react-router-dom';
import { FileText, User, MessageSquare, LayoutDashboard } from 'lucide-react';
import Dashboard from './pages/Dashboard';
import Resume from './pages/Resume';
import Interview from './pages/Interview';
import Login from './pages/Login';

const NavigationLink = ({ to, icon: Icon, children }: any) => {
  const navigate = useNavigate();
  const location = useLocation();
  const isActive = location.pathname === to;

  const handleClick = (e: any) => {
    e.preventDefault();
    if (sessionStorage.getItem('isInterviewing') === 'true') {
      alert("Please finish or terminate your current interview before navigating away.");
      return;
    }
    navigate(to);
  };

  return (
    <a href={to} onClick={handleClick} className={`flex items-center gap-3 px-4 py-3 rounded-xl transition-all ${isActive ? 'bg-primary/20 text-white' : 'text-muted hover:text-white hover:bg-white/5'}`}>
      <Icon size={20} />
      <span>{children}</span>
    </a>
  );
};

function App() {
  return (
    <Router>
      <div className="min-h-screen flex flex-col md:flex-row bg-background bg-gradient-radial from-surface/50 to-background">
        
        {/* Sidebar Navigation */}
        <aside className="w-full md:w-64 glass-panel border-l-0 border-y-0 rounded-none md:rounded-r-2xl flex flex-col p-6 z-10 relative">
          <div className="flex items-center gap-3 mb-10">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-primary to-accent flex items-center justify-center text-white font-bold text-xl shadow-lg shadow-primary/30">
              AI
            </div>
            <h1 className="text-xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-white to-white/70">Placement<br/>Platform</h1>
          </div>
          
          <nav className="flex-1 space-y-2">
            <NavigationLink to="/" icon={LayoutDashboard}>Dashboard</NavigationLink>
            <NavigationLink to="/resume" icon={FileText}>Resume Analysis</NavigationLink>
            <NavigationLink to="/interview" icon={MessageSquare}>Mock Interview</NavigationLink>
          </nav>

          <div className="mt-auto">
            <button className="flex items-center gap-3 px-4 py-3 w-full rounded-xl text-muted hover:text-white hover:bg-white/5 transition-all text-left">
              <User size={20} />
              <span>Profile</span>
            </button>
          </div>
        </aside>

        {/* Main Content Area */}
        <main className="flex-1 p-6 md:p-12 overflow-y-auto relative z-0">
          <Routes>
            <Route path="/login" element={<Login />} />
            <Route path="/" element={<Dashboard />} />
            <Route path="/resume" element={<Resume />} />
            <Route path="/interview" element={<Interview />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
