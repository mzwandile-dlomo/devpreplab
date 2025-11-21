import { render, screen, fireEvent } from "@testing-library/react";
import React from "react";
import RootLayout from "../../app/layout";

const mockSetIsMenuOpen = jest.fn();
jest.mock("react", () => ({
  ...jest.requireActual("react"),
  useState: (initialValue: any) => [initialValue, mockSetIsMenuOpen],
}));

function renderWithLayout(children: React.ReactNode) {
  return render(<RootLayout>{children}</RootLayout>);
}

describe("Root layout navbar", () => {
  it("renders brand and navigation links", () => {
    renderWithLayout("Content");

    const brandLink = screen.getByRole("link", { name: /DevPrepLab/i });
    expect(brandLink).toBeInTheDocument();

    const homeLink = screen.getByRole("link", { name: /home/i });
    const problemsLink = screen.getByRole("link", { name: /problems/i });

    expect(homeLink).toHaveAttribute("href", "/");
    expect(problemsLink).toHaveAttribute("href", "/problems");
  });

  it("toggles menu on hamburger button click", () => {
    renderWithLayout("Content");

    const hamburgerButton = screen.getByRole("button");
    fireEvent.click(hamburgerButton);

    expect(mockSetIsMenuOpen).toHaveBeenCalled();
  });
});