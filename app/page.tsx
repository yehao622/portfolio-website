import Header from '@/components/Header';
import Hero from '@/components/Hero';
import ProjectCard from '@/components/ProjectCard';
import AIChat from '@/components/AIChat';
import { projects } from '@/lib/projects';

export default function Home() {
  return (
    <main className="min-h-screen bg-gradient-to-b from-slate-50 to-slate-100">
      <Header />
      <Hero />

      {/* About section */}
      <section id="about" className="max-w-6xl mx-auto px-4 py-20">
        <h3 className="text-3xl font-bold text-slate-900 mb-6">About Me</h3>
        <div className="grid md:grid-cols-2 gap-8">
          <div>
            <p className="text-slate-700 mb-4">
              Results-driven DevOps/DevSecOps Engineer and MS Computer Engineering graduate (University of Tennessee Knoxville, 2025). 
              I specialize in bridging software engineering and IT operations to deliver scalable, production-ready solutions.
            </p>
            <p className="text-slate-700 mb-4">
              Passionate about building automated CI/CD pipelines, secure containerized microservices, and resilient cloud infrastructures. 
              My recent experience spans infrastructure automation (Ansible, Terraform), application security (RBAC, JWT, rate limiting), 
              and deploying full-stack, AI-integrated platforms using the Google Gemini API.
            </p>
          </div>
          <div>
            <h4 className="font-semibold text-slate-900 mb-3">Core Competencies</h4>
            <ul className="space-y-2 text-slate-700">
              <li>• <strong>CI/CD & Automation:</strong> GitHub Actions, Jenkins, Ansible, Terraform</li>
              <li>• <strong>Cloud & Containers:</strong> AWS, Docker, Kubernetes, Render, Vercel</li>
              <li>• <strong>DevSecOps:</strong> RBAC, JWT, SSH Hardening, API Key Auth, Rate Limiting</li>
              <li>• <strong>Full Stack Development:</strong> TypeScript, Node.js, React, C/C++</li>
              <li>• <strong>AI Integration:</strong> Google Gemini API, PyTorch, Hugging Face</li>
              <li>• <strong>HPC & Systems:</strong> Distributed Systems Performance Modeling</li>
            </ul>
          </div>
        </div>
      </section>

      {/* Projects Section - NOW WITH REAL CONTENT */}
      <section id="projects" className="bg-white py-20">
        <div className="max-w-6xl mx-auto px-4">
          <h3 className="text-3xl font-bold text-slate-900 mb-4 text-center">Featured Projects</h3>
          <p className="text-slate-600 text-center mb-12 max-w-2xl mx-auto">
            Showcasing scalable systems, AI integration, and performance optimization across cloud and HPC domains.
          </p>

          {/* Project Cards Grid */}
          <div className="grid md:grid-cols-2 gap-8 max-w-5xl mx-auto">
            {projects.map((project) => (
              <ProjectCard key={project.id} project={project} />
            ))}
          </div>
        </div>
      </section>

      {/* Contact Section */}
      <section id="contact" className="max-w-6xl mx-auto px-4 py-20">
        <h3 className="text-3xl font-bold text-slate-900 mb-6 text-center">Get In Touch</h3>
        <div className="max-w-2xl mx-auto text-center">
          <p className="text-slate-700 mb-6">
            I'm currently seeking junior to entry/mid-level positions in DevOps, Full Stack, Cloud,
            and System Performance engineering. Open to full/part-time, contract, and remote opportunities.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <a
              href="mailto:hyedailyuse@gmail.com"
              className="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 transition"
            >
              Email Me
            </a>
            <a
              href="https://www.linkedin.com/in/ye-hao-256168121/"
              target="_blank"
              rel="noopener noreferrer"
              className="bg-slate-200 text-slate-800 px-6 py-3 rounded-lg hover:bg-slate-300 transition"
            >
              Connect on LinkedIn
            </a>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-slate-900 text-slate-400 py-8">
        <div className="max-w-6xl mx-auto px-4 text-center">
          <p>© 2025 Howard(Hao) Ye. Built with Next.js, TypeScript, and Tailwind CSS.</p>
        </div>
      </footer>

      {/* AI Chat Floating Button */}
      <AIChat />
    </main>
  );
}
