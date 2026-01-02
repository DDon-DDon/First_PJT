
import MainHeader from "./components/main/MainHeader"
import Sidebar, { SidebarNavItem } from './components/main/Sidebar';
import DashboardPage from './components/main/DashboardPage';

export default function MainPage() {
  return (
    <div className="flex h-screen w-full bg-slate-50 dark:bg-[#101922] text-slate-900 dark:text-white font-sans overflow-hidden">
      {/* Side Bar */}
      <Sidebar />
      {/* Main Content */}
      <main className="flex-1 flex flex-col h-full overflow-hidden">
        {/* Header */}
        <MainHeader />
        {/* Dashboard Scroll Area */}
        <DashboardPage />
      </main>
    </div>
  );
}
