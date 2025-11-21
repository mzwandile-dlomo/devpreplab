import * as React from "react";

const Link = ({ href, children, ...rest }: React.PropsWithChildren<{ href: string }>) => {
  return (
    <a href={href} {...rest}>
      {children}
    </a>
  );
};

export default Link;