import { useState, useRef, useEffect } from "react";

const ResizableSidebar = ({
  initialWidth = 400,
  minWidth = 0,
  maxWidth = 600,
  children,
}) => {
  const [sidebarWidth, setSidebarWidth] = useState(initialWidth);
  const isResizing = useRef(false);
  const sidebarRef = useRef(null);

  const handleMouseDown = () => {
    isResizing.current = true;
  };

  useEffect(() => {
    const handleMouseMove = (e) => {
      if (!isResizing.current) return;
      const newWidth = window.innerWidth - e.clientX;
      if (newWidth >= minWidth && newWidth <= maxWidth) {
        setSidebarWidth(newWidth);
      }
    };

    const handleMouseUp = () => {
      isResizing.current = false;
    };

    document.addEventListener("mousemove", handleMouseMove);
    document.addEventListener("mouseup", handleMouseUp);

    return () => {
      document.removeEventListener("mousemove", handleMouseMove);
      document.removeEventListener("mouseup", handleMouseUp);
    };
  }, [minWidth, maxWidth]);

  return (
    <div
      ref={sidebarRef}
      style={{
        position: "absolute",
        top: 0,
        right: 0,
        width: `${sidebarWidth}px`,
        height: "100%",
        background: "#fff",
        boxShadow: "-4px 0 12px rgba(0,0,0,0.2)",
        zIndex: 9999,
        overflowY: "auto",
      }}
    >
      {/* 드래그 핸들 */}
      <div
        onMouseDown={handleMouseDown}
        style={{
          width: "5px",
          cursor: "ew-resize",
          position: "absolute",
          left: 0,
          top: 0,
          bottom: 0,
          zIndex: 10000,
        }}
      ></div>

      {children}
    </div>
  );
};

export default ResizableSidebar;
