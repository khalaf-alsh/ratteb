import { Outlet } from "react-router-dom";
import Header from "./Header";
import "./AppLayout.css";

function AppLayout() {
  return (
    <div className="app-layout">
      <div className="app-main">
        <Header />

        <main className="page-content">
          <Outlet />
        </main>
      </div>
    </div>
  );
}

export default AppLayout;
