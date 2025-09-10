import React from 'react';

interface ViewPortProps {
  children?: React.ReactNode;
}

const ViewPort: React.FC<ViewPortProps> = ({ children }) => {
  return (
    <div className="w-screen h-screen bg-base-900 flex items-center justify-center">
        <div className="rounded-lg bg-base-200 w-[90vw] h-[90vh] p-[5%] overflow-auto flex flex-col">
            {children}
        </div>
    </div>
  );
};

export default ViewPort;