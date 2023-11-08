import React, { useState, useEffect, useMemo } from "react";
import { BrowserRouter as Router, useLocation } from "react-router-dom"
import styled from "styled-components";
import { FractalProvider } from "./contexts/FractalContext";
import FullViewFractal from "./components/FullViewFractal";

const App = () => {

	return (
		<Router>
			<FractalProvider>
				<Background>
					<FullViewFractal />
				</Background>
			</FractalProvider>
		</Router>
	);
};

const Background = styled.div`
	background-color: #222222;
	width: 100vw;
	height: 100vh;
`;

export default App;
