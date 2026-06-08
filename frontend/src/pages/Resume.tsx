import React, { useState } from 'react';
import { UploadCloud, FileText, CheckCircle2, AlertTriangle, Search, Star, Target, Briefcase, Layout } from 'lucide-react';
import api from '../api/axios';

export default function Resume() {
  const [file, setFile] = useState<File | null>(null);
  const [jobDescription, setJobDescription] = useState<string>('');
  const [isUploading, setIsUploading] = useState(false);
  const [results, setResults] = useState<any>(null);
  const [errorMsg, setErrorMsg] = useState<string>('');
  
  const [searchQuery, setSearchQuery] = useState("");
  const [searchResults, setSearchResults] = useState<any[]>([]);

  const handleUpload = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!file || !jobDescription.trim()) {
      setErrorMsg("Please provide both a resume file and a job description.");
      return;
    }
    
    setIsUploading(true);
    setErrorMsg('');
    try {
      const formData = new FormData();
      formData.append('file', file);
      formData.append('job_description', jobDescription);
      
      const res = await api.post('/resume/upload', formData);
      
      setResults(res.data);
    } catch (error: any) {
      console.error(error);
      let errDetail = error.response?.data?.detail;
      if (Array.isArray(errDetail)) {
        errDetail = errDetail.map((e: any) => `${e.loc?.join('.') || 'Field'}: ${e.msg}`).join(', ');
      } else if (typeof errDetail === 'object' && errDetail !== null) {
        errDetail = JSON.stringify(errDetail);
      }
      setErrorMsg(errDetail || "An error occurred while analyzing the resume.");
    } finally {
      setIsUploading(false);
    }
  };

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!searchQuery) return;
    try {
      const res = await api.get(`/resume/search?query=${encodeURIComponent(searchQuery)}`);
      setSearchResults(res.data.results || []);
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div className="space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-700">
      <header>
        <h1 className="text-4xl font-bold mb-2">Resume Intelligence</h1>
        <p className="text-muted">Upload your resume for AI-powered analysis and semantic matching.</p>
      </header>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <div className="glass-panel p-8">
          <h2 className="text-2xl font-semibold mb-6">Upload Resume</h2>
          
          <form onSubmit={handleUpload} className="space-y-6">
            <div className="space-y-2">
              <label className="text-sm font-medium text-white/80">Job Description</label>
              <textarea 
                className="w-full bg-background/50 border border-white/10 rounded-xl p-4 text-white focus:outline-none focus:border-primary transition-colors min-h-[120px]"
                placeholder="Paste the job description here..."
                value={jobDescription}
                onChange={(e) => setJobDescription(e.target.value)}
                required
              />
            </div>

            <div className="space-y-2">
              <label className="text-sm font-medium text-white/80">Resume File (PDF/DOCX)</label>
              <div className="border-2 border-dashed border-white/20 rounded-2xl p-10 text-center hover:bg-white/5 transition-colors cursor-pointer"
                   onClick={() => document.getElementById('file-upload')?.click()}>
                <input 
                  id="file-upload" 
                  type="file" 
                  className="hidden" 
                  accept=".pdf,.docx"
                  onChange={(e) => setFile(e.target.files?.[0] || null)}
                />
                <UploadCloud size={48} className="mx-auto text-primary mb-4" />
                {file ? (
                  <p className="text-white font-medium">{file.name}</p>
                ) : (
                  <>
                    <p className="text-white font-medium mb-1">Click to upload or drag and drop</p>
                    <p className="text-muted text-sm">PDF or DOCX (MAX. 5MB)</p>
                  </>
                )}
              </div>
            </div>
            
            {errorMsg && (
              <div className="bg-red-500/10 border border-red-500/20 text-red-400 p-3 rounded-lg text-sm flex items-center gap-2">
                <AlertTriangle size={16} /> {errorMsg}
              </div>
            )}

            <button 
              type="submit" 
              disabled={!file || !jobDescription.trim() || isUploading}
              className="btn-primary w-full flex justify-center items-center gap-2"
            >
              {isUploading ? (
                <span className="animate-pulse flex items-center gap-2">
                  <div className="w-4 h-4 border-2 border-white/20 border-t-white rounded-full animate-spin" />
                  Analyzing Resume with AI...
                </span>
              ) : (
                <>Analyze Resume <FileText size={18} /></>
              )}
            </button>
          </form>
        </div>

        {results && (
          <div className="glass-panel p-8 bg-gradient-to-br from-surface/80 to-surface overflow-y-auto max-h-[800px] custom-scrollbar">
            <h2 className="text-2xl font-semibold mb-6 flex items-center gap-2"><Star className="text-yellow-400" /> Analysis Results</h2>
            
            <div className="flex items-center gap-6 mb-8">
              <div className="relative w-28 h-28 flex items-center justify-center rounded-full border-4 border-primary/20">
                <svg className="absolute inset-0 w-full h-full transform -rotate-90">
                  <circle cx="52" cy="52" r="52" stroke="currentColor" strokeWidth="8" fill="transparent" className="text-primary/20" />
                  <circle cx="52" cy="52" r="52" stroke="currentColor" strokeWidth="8" fill="transparent" strokeDasharray={`${results.ats_score * 3.26} 326`} className="text-primary transition-all duration-1000" />
                </svg>
                <div className="text-center">
                  <span className="text-4xl font-bold">{results.ats_score}</span>
                  <span className="block text-xs text-muted">/ 100</span>
                </div>
              </div>
              <div>
                <h3 className="text-xl font-bold">Overall ATS Score</h3>
                <p className="text-muted">Based on your provided job description.</p>
              </div>
            </div>

            <div className="grid grid-cols-2 gap-4 mb-8">
              <div className="bg-white/5 p-4 rounded-xl border border-white/5">
                <h4 className="text-sm font-semibold text-muted flex items-center gap-2 mb-2"><Target size={14}/> Skills Match</h4>
                <div className="flex items-end gap-2"><span className="text-2xl font-bold">{results.skills_match}%</span></div>
              </div>
              <div className="bg-white/5 p-4 rounded-xl border border-white/5">
                <h4 className="text-sm font-semibold text-muted flex items-center gap-2 mb-2"><Briefcase size={14}/> Experience</h4>
                <div className="flex items-end gap-2"><span className="text-2xl font-bold">{results.experience_match}%</span></div>
              </div>
              <div className="bg-white/5 p-4 rounded-xl border border-white/5">
                <h4 className="text-sm font-semibold text-muted flex items-center gap-2 mb-2"><Search size={14}/> Keywords</h4>
                <div className="flex items-end gap-2"><span className="text-2xl font-bold">{results.keyword_match}%</span></div>
              </div>
              <div className="bg-white/5 p-4 rounded-xl border border-white/5">
                <h4 className="text-sm font-semibold text-muted flex items-center gap-2 mb-2"><Layout size={14}/> Formatting</h4>
                <div className="flex items-end gap-2"><span className="text-2xl font-bold">{results.formatting_score}%</span></div>
              </div>
            </div>

            <div className="space-y-6">
              {results.matched_skills && results.matched_skills.length > 0 && (
                <div>
                  <h4 className="font-semibold text-white/90 mb-3 flex items-center gap-2"><CheckCircle2 size={18} className="text-green-500"/> Matched Skills</h4>
                  <div className="flex flex-wrap gap-2">
                    {results.matched_skills.map((s: string, i: number) => (
                      <span key={i} className="px-3 py-1 rounded-full bg-green-500/10 text-green-400 text-sm border border-green-500/20">{s}</span>
                    ))}
                  </div>
                </div>
              )}

              {results.missing_skills && results.missing_skills.length > 0 && (
                <div>
                  <h4 className="font-semibold text-white/90 mb-3 flex items-center gap-2"><AlertTriangle size={18} className="text-red-500"/> Missing Skills (Critical)</h4>
                  <div className="flex flex-wrap gap-2">
                    {results.missing_skills.map((s: string, i: number) => (
                      <span key={i} className="px-3 py-1 rounded-full bg-red-500/10 text-red-400 text-sm border border-red-500/20">{s}</span>
                    ))}
                  </div>
                </div>
              )}

              {results.strengths && results.strengths.length > 0 && (
                <div>
                  <h4 className="font-semibold text-white/90 mb-3">💪 Key Strengths</h4>
                  <ul className="space-y-2 text-sm text-muted">
                    {results.strengths.map((r: string, i: number) => (
                      <li key={i} className="flex gap-2"><span className="text-primary">•</span> {r}</li>
                    ))}
                  </ul>
                </div>
              )}

              {results.recommendations && results.recommendations.length > 0 && (
                <div>
                  <h4 className="font-semibold text-white/90 mb-3">📈 Improvement Suggestions</h4>
                  <ul className="space-y-2 text-sm text-muted">
                    {results.recommendations.map((r: string, i: number) => (
                      <li key={i} className="flex gap-2"><span className="text-accent">•</span> {r}</li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          </div>
        )}
      </div>

      <div className="glass-panel p-8 mt-8">
        <h2 className="text-2xl font-semibold mb-6 flex items-center gap-2"><Search className="text-accent" /> Semantic Resume Search</h2>
        <form onSubmit={handleSearch} className="flex gap-4 mb-6">
          <input 
            type="text" 
            placeholder="Search for 'React developer with 3 years experience'..." 
            className="input-field"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
          />
          <button type="submit" className="btn-primary whitespace-nowrap">Search</button>
        </form>

        {searchResults.length > 0 && (
          <div className="space-y-4">
            {searchResults.map((res, i) => (
              <div key={i} className="p-4 rounded-xl bg-background/50 border border-white/5 flex justify-between items-center">
                <div>
                  <p className="font-medium text-white/90">Resume #{res.resume_id}</p>
                  <p className="text-sm text-muted">{res.content_preview}</p>
                </div>
                <div className="text-right">
                  <span className="text-accent font-bold text-lg">{(res.similarity_score * 100).toFixed(0)}%</span>
                  <p className="text-xs text-muted">Match</p>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
