import { useState, useEffect } from 'react';
import { Play, CheckCircle2, AlertTriangle, XCircle, BarChart3, AlertCircle, BookOpen } from 'lucide-react';
import api from '../api/axios';

const DOMAINS = [
  "Frontend Development", "Backend Development", "Full Stack Development",
  "React.js", "Node.js", "Java", "Python", "Data Structures & Algorithms",
  "Database/SQL", "AI/ML", "Data Science", "Cloud & DevOps",
  "Cybersecurity", "Aptitude & HR Interview"
];

const DIFFICULTIES = ["Beginner", "Intermediate", "Advanced"];

export default function Interview() {
  const [step, setStep] = useState<'setup' | 'active' | 'loading' | 'results'>('setup');
  
  // Setup State
  const [domain, setDomain] = useState(DOMAINS[0]);
  const [difficulty, setDifficulty] = useState("Intermediate");
  const [numQuestions, setNumQuestions] = useState(10);
  
  // Interview State
  const [questions, setQuestions] = useState<string[]>([]);
  const [answers, setAnswers] = useState<string[]>([]);
  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [currentAnswer, setCurrentAnswer] = useState("");
  const [violationCount, setViolationCount] = useState(0);
  const [warningModal, setWarningModal] = useState(false);
  
  // Results State
  const [results, setResults] = useState<any>(null);

  // Anti-Cheating: Tab Tracking
  useEffect(() => {
    if (step !== 'active') return;

    const handleVisibilityChange = () => {
      if (document.hidden) {
        setViolationCount(prev => {
          const nextCount = prev + 1;
          if (nextCount >= 3) {
            terminateInterview(nextCount);
          } else {
            setWarningModal(true);
          }
          return nextCount;
        });
      }
    };

    document.addEventListener("visibilitychange", handleVisibilityChange);
    return () => document.removeEventListener("visibilitychange", handleVisibilityChange);
  }, [step, questions, answers, currentAnswer]);

  // Anti-Cheating: Prevent Back Navigation
  useEffect(() => {
    if (step === 'active') {
      window.history.pushState(null, '', window.location.href);
      const handlePopState = () => {
        window.history.pushState(null, '', window.location.href);
        alert("Back navigation is disabled during an active interview.");
      };
      window.addEventListener('popstate', handlePopState);
      return () => window.removeEventListener('popstate', handlePopState);
    }
  }, [step]);

  const startInterview = async () => {
    setStep('loading');
    sessionStorage.setItem('isInterviewing', 'true');
    setViolationCount(0);
    setAnswers([]);
    setCurrentQuestion(0);
    setCurrentAnswer("");

    try {
      const response = await api.post("/interview/generate", {
        profile: "Software Engineer",
        topic: domain,
        domain: domain,
        difficulty: difficulty.toLowerCase(),
        num_questions: numQuestions
      });
      setQuestions(response.data.questions);
      setStep('active');
    } catch (error: any) {
      console.error("API Error generating questions:", error);
      let errMsg = "Failed to generate questions. ";
      if (error.code === 'ERR_NETWORK') {
        errMsg += "Backend server is unreachable. Please ensure the backend is running and properly configured.";
      } else if (error.response) {
        errMsg += error.response.data?.detail || `Server error (${error.response.status}).`;
      }
      alert(errMsg);
      setStep('setup');
      sessionStorage.removeItem('isInterviewing');
    }
  };

  const terminateInterview = async (strikes: number) => {
    setStep('loading');
    sessionStorage.removeItem('isInterviewing');
    alert(`Interview terminated due to ${strikes} tab-switching violations.`);
    
    // Submit whatever we have so far
    const finalAnswers = [...answers, currentAnswer];
    submitEvaluation(finalAnswers, "Terminated");
  };

  const nextQuestion = () => {
    const newAnswers = [...answers, currentAnswer];
    setAnswers(newAnswers);
    setCurrentAnswer("");
    
    if (currentQuestion < questions.length - 1) {
      setCurrentQuestion(prev => prev + 1);
    } else {
      setStep('loading');
      sessionStorage.removeItem('isInterviewing');
      submitEvaluation(newAnswers, "Completed");
    }
  };

  const submitEvaluation = async (finalAnswers: string[], status: string) => {
    try {
      const response = await api.post("/interview/evaluate", {
        questions: questions.slice(0, finalAnswers.length),
        answers: finalAnswers,
        domain: domain,
        status: status
      });
      setResults(response.data);
      setStep('results');
    } catch (error: any) {
      console.error("API Error evaluating interview:", error);
      let errMsg = "Failed to evaluate interview. ";
      if (error.code === 'ERR_NETWORK') {
        errMsg += "Backend server is unreachable. Please ensure the backend is running and properly configured.";
      } else if (error.response) {
        errMsg += error.response.data?.detail || `Server error (${error.response.status}).`;
      }
      alert(errMsg);
      setStep('setup');
    }
  };

  if (step === 'loading') {
    return (
      <div className="flex flex-col items-center justify-center min-h-[60vh] space-y-6">
        <div className="w-16 h-16 border-4 border-primary border-t-transparent rounded-full animate-spin"></div>
        <h2 className="text-2xl font-semibold">Processing AI Models...</h2>
        <p className="text-muted">This may take a moment.</p>
      </div>
    );
  }

  if (step === 'results' && results) {
    const isTerminated = results.status === "Terminated";
    return (
      <div className="space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-700 max-w-5xl mx-auto">
        <header className="text-center mb-8">
          <div className="inline-flex items-center justify-center p-4 rounded-full bg-primary/20 text-primary mb-4">
            <BarChart3 size={32} />
          </div>
          <h1 className="text-4xl font-bold mb-2">Interview Results</h1>
          {isTerminated ? (
            <p className="text-red-400 font-semibold text-lg flex items-center justify-center gap-2">
              <XCircle size={20} /> Interview Terminated (Anti-Cheat Violation)
            </p>
          ) : (
            <p className="text-green-400 font-semibold text-lg flex items-center justify-center gap-2">
              <CheckCircle2 size={20} /> Interview Completed Successfully
            </p>
          )}
        </header>

        <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
          <ScoreCard title="Overall Score" score={results.overall_score} />
          <ScoreCard title="Technical" score={results.technical_score} />
          <ScoreCard title="Communication" score={results.communication_score} />
          <ScoreCard title="Confidence" score={results.confidence_score} />
        </div>

        <div className="glass-panel p-6 border-l-4 border-l-primary">
          <h3 className="font-semibold text-lg mb-2">Domain Performance: {domain}</h3>
          <p className="text-muted leading-relaxed">{results.domain_performance}</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="glass-panel p-6">
            <h3 className="font-semibold text-lg mb-4 flex items-center gap-2 text-green-400">
              <CheckCircle2 size={20} /> Strengths
            </h3>
            <ul className="space-y-3">
              {results.strengths.map((s: string, i: number) => (
                <li key={i} className="flex items-start gap-3 text-sm text-muted">
                  <div className="w-1.5 h-1.5 rounded-full bg-green-500 mt-1.5" />
                  {s}
                </li>
              ))}
            </ul>
          </div>
          <div className="glass-panel p-6">
            <h3 className="font-semibold text-lg mb-4 flex items-center gap-2 text-yellow-400">
              <AlertTriangle size={20} /> Areas to Improve
            </h3>
            <ul className="space-y-3">
              {results.areas_to_improve.map((s: string, i: number) => (
                <li key={i} className="flex items-start gap-3 text-sm text-muted">
                  <div className="w-1.5 h-1.5 rounded-full bg-yellow-500 mt-1.5" />
                  {s}
                </li>
              ))}
            </ul>
          </div>
        </div>

        <div className="glass-panel p-6">
          <h3 className="font-semibold text-lg mb-4 flex items-center gap-2 text-blue-400">
            <BookOpen size={20} /> Recommended Learning Resources
          </h3>
          <ul className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {results.learning_resources.map((r: string, i: number) => (
              <li key={i} className="p-4 bg-white/5 rounded-lg border border-white/10 text-sm text-muted">
                {r}
              </li>
            ))}
          </ul>
        </div>

        <div className="text-center mt-8">
          <button onClick={() => setStep('setup')} className="btn-primary">
            Start New Interview
          </button>
        </div>
      </div>
    );
  }

  if (step === 'active') {
    return (
      <div className="space-y-6 max-w-4xl mx-auto">
        {/* Active Banner */}
        <div className="bg-red-500/20 border border-red-500/50 text-red-200 px-6 py-3 rounded-xl flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-2 h-2 rounded-full bg-red-500 animate-pulse" />
            <span className="font-medium">Interview in Progress - Do not switch tabs or navigate away</span>
          </div>
          <span className="text-sm font-semibold bg-red-500/30 px-3 py-1 rounded-full text-red-100">
            Violations: {violationCount}/3
          </span>
        </div>

        {warningModal && (
          <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/80 backdrop-blur-sm">
            <div className="bg-[#1a1f2e] border border-red-500/30 p-8 rounded-2xl max-w-md w-full shadow-2xl">
              <div className="w-16 h-16 rounded-full bg-red-500/20 text-red-500 flex items-center justify-center mx-auto mb-6">
                <AlertCircle size={32} />
              </div>
              <h3 className="text-2xl font-bold text-center mb-2">Warning!</h3>
              <p className="text-muted text-center mb-6">
                You have switched tabs or minimized the browser. This is violation {violationCount} of 3. 
                If you reach 3 violations, the interview will be automatically terminated.
              </p>
              <button onClick={() => setWarningModal(false)} className="btn-primary w-full bg-red-600 hover:bg-red-700 text-white">
                I Understand
              </button>
            </div>
          </div>
        )}

        <div className="glass-panel p-8 relative overflow-hidden">
          <div className="absolute top-0 left-0 w-full h-1 bg-white/10">
            <div 
              className="h-full bg-primary transition-all duration-500" 
              style={{ width: `${((currentQuestion + 1) / questions.length) * 100}%` }}
            />
          </div>
          
          <div className="flex justify-between items-center mb-8 text-sm font-medium text-muted">
            <span>Question {currentQuestion + 1} of {questions.length}</span>
            <span className="text-primary px-3 py-1 rounded-full bg-primary/10">{domain}</span>
          </div>
          
          <h2 className="text-2xl font-semibold mb-8 leading-relaxed">
            "{questions[currentQuestion]}"
          </h2>
          
          <div className="space-y-4">
            <textarea 
              className="input-field min-h-[200px] resize-none text-lg leading-relaxed p-6"
              placeholder="Type your detailed answer here..."
              value={currentAnswer}
              onChange={(e) => setCurrentAnswer(e.target.value)}
              onPaste={(e) => {
                e.preventDefault();
                alert("Pasting is disabled during the interview.");
              }}
            />
            
            <div className="flex justify-end pt-4">
              <button 
                className="btn-primary px-8 py-3"
                onClick={nextQuestion}
                disabled={currentAnswer.trim().length < 10}
              >
                {currentQuestion < questions.length - 1 ? 'Submit & Next Question' : 'Submit & Finish Interview'}
              </button>
            </div>
          </div>
        </div>
      </div>
    );
  }

  // Setup Step
  return (
    <div className="space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-700 max-w-4xl mx-auto">
      <header className="text-center mb-12">
        <h1 className="text-4xl font-bold mb-4">AI Mock Interview</h1>
        <p className="text-muted max-w-2xl mx-auto">Configure your mock interview session. Our AI will generate unique questions tailored to your domain and dynamically evaluate your performance.</p>
      </header>

      <div className="glass-panel p-10">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mb-10">
          <div className="space-y-3">
            <label className="text-sm font-medium text-white/80">Select Domain</label>
            <select 
              className="input-field w-full appearance-none bg-[#1a1f2e]"
              value={domain}
              onChange={(e) => setDomain(e.target.value)}
            >
              {DOMAINS.map(d => <option key={d} value={d}>{d}</option>)}
            </select>
          </div>
          
          <div className="space-y-3">
            <label className="text-sm font-medium text-white/80">Difficulty Level</label>
            <select 
              className="input-field w-full appearance-none bg-[#1a1f2e]"
              value={difficulty}
              onChange={(e) => setDifficulty(e.target.value)}
            >
              {DIFFICULTIES.map(d => <option key={d} value={d}>{d}</option>)}
            </select>
          </div>
        </div>

        <div className="space-y-4 mb-12">
          <label className="text-sm font-medium text-white/80 block">Number of Questions</label>
          <div className="flex gap-4">
            {[10, 15, 20].map(num => (
              <button
                key={num}
                onClick={() => setNumQuestions(num)}
                className={`flex-1 py-4 rounded-xl border transition-all ${
                  numQuestions === num 
                  ? 'border-primary bg-primary/20 text-primary font-bold' 
                  : 'border-white/10 hover:border-white/30 text-muted'
                }`}
              >
                {num} Questions
              </button>
            ))}
          </div>
        </div>

        <div className="bg-yellow-500/10 border border-yellow-500/20 p-6 rounded-xl mb-10 text-sm text-yellow-200/80">
          <h4 className="font-bold text-yellow-500 mb-2 flex items-center gap-2">
            <AlertTriangle size={18} /> Anti-Cheat System Active
          </h4>
          <ul className="list-disc pl-5 space-y-1">
            <li>Do not switch browser tabs or minimize the window.</li>
            <li>Copy-pasting is disabled during the interview.</li>
            <li>3 violations will result in immediate termination.</li>
          </ul>
        </div>

        <div className="text-center">
          <button 
            onClick={startInterview}
            className="btn-primary px-12 py-4 text-lg inline-flex items-center gap-3 font-semibold shadow-lg shadow-primary/20 hover:shadow-primary/40 hover:-translate-y-1 transition-all"
          >
            Start Interview <Play size={24} fill="currentColor" />
          </button>
        </div>
      </div>
    </div>
  );
}

const ScoreCard = ({ title, score }: { title: string, score: number }) => {
  const getColor = (s: number) => {
    if (s >= 80) return 'text-green-400';
    if (s >= 60) return 'text-yellow-400';
    return 'text-red-400';
  };
  
  return (
    <div className="glass-panel p-6 text-center flex flex-col items-center justify-center">
      <h3 className="text-sm font-medium text-muted mb-2">{title}</h3>
      <div className={`text-4xl font-bold ${getColor(score)}`}>
        {score}<span className="text-lg opacity-50">/100</span>
      </div>
    </div>
  );
};
