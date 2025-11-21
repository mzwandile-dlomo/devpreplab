import { render, screen } from "@testing-library/react";
import Home from "../../app/page";

describe("Home page", () => {
  it("renders hero copy and Browse problems link", () => {
    render(<Home />);

    expect(
      screen.getByText(/Practice coding interviews with focused, timed challenges./i)
    ).toBeInTheDocument();

    const browseLink = screen.getByRole("link", { name: /browse problems/i });
    expect(browseLink).toBeInTheDocument();
    expect(browseLink).toHaveAttribute("href", "/problems");
  });
});