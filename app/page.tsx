import Header from '@/components/Header';
import Hero from '@/components/Hero';
import ProjectCard from '@/components/ProjectCard';
import { projects } from '@/lib/projects'

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
              Computer Engineering graduate student at University of Tennessee Knoxville, graduating May 2025.
              Previous MS in Industrial Engineering with focus on optimization and mathematical modeling.
            </p>
            <p className="text-slate-700 mb-4">
              Passionate about building scalable cloud infrastructure, DevOps automation, and AI-powered systems.
              Experience spans Python backend development, microservices architecture, AWS cloud services, and
              high-performance computing simulation.
            </p>
          </div>
          <div>
            <h4 className="font-semibold text-slate-900 mb-3">Core Competencies</h4>
            <ul className="space-y-2 text-slate-700">
              <li>• Cloud Infrastructure (AWS, Docker, PostgreSQL)</li>
              <li>• Full Stack Development (Python, Node.js, React)</li>
              <li>• AI/ML Integration (LangChain, OpenAI, RAG)</li>
              <li>• DevOps & CI/CD Automation</li>
              <li>• High-Performance Computing</li>
              <li>• System Performance Optimization</li>
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
    </main>
  );
}
