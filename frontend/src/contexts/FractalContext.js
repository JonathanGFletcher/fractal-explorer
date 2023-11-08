import React, { createContext, useContext, useEffect, useState, useMemo } from "react";
import { useLocation } from "react-router-dom";
import * as Constants from "../Constants"

const FractalContext = createContext();
const FractalUpdateContext = createContext();

export const useFractalContext = () => useContext(FractalContext);
export const useFractalUpdateContext = () => useContext(FractalUpdateContext);

const useQuery = () => {
	const { search } = useLocation();
	return useMemo(() => new URLSearchParams(search), [search]);
}

export const FractalProvider = ({ children }) => {

    // ?type=julia&constant_x=-0.8&constant_y=0.156&center_x=0.0&center_y=0.0&scale=1.0&iterations=500&samples=1&width=3000&height=2000
    let query = useQuery();
    const fractalType = query.get("type") || Constants.DEFAULT_FULL_VIEW_PARAMS.type;
    const fractalConstantX = query.get("constant_x") || Constants.DEFAULT_FULL_VIEW_PARAMS.constant_x;
    const fractalConstantY = query.get("constant_y") || Constants.DEFAULT_FULL_VIEW_PARAMS.constant_y;
    const fractalCenterX = query.get("center_x") || Constants.DEFAULT_FULL_VIEW_PARAMS.center_x;
    const fractalCenterY = query.get("center_y") || Constants.DEFAULT_FULL_VIEW_PARAMS.center_y;
    const fractalScale = query.get("scale") || Constants.DEFAULT_FULL_VIEW_PARAMS.scale;
    const fractalIterations = query.get("iterations") || Constants.DEFAULT_FULL_VIEW_PARAMS.iterations;
    const fractalSamples = query.get("samples") || Constants.DEFAULT_FULL_VIEW_PARAMS.samples;
    const fractalWidth = query.get("render_width") || Constants.DEFAULT_FULL_VIEW_PARAMS.dimensions.width;
    const fractalHeight = query.get("render_height") || Constants.DEFAULT_FULL_VIEW_PARAMS.dimensions.height;

    const [fullViewParams, setFullViewParams] = useState({
        type: fractalType,
        constant: { x: Number(fractalConstantX), y: Number(fractalConstantY) },
        center: { x: Number(fractalCenterX), y: Number(fractalCenterY) },
        scale: Number(fractalScale),
        iterations: Number(fractalIterations),
        samples: Number(fractalSamples),
        dimensions: {
            width: Number(fractalWidth),
            height: Number(fractalHeight),
        },
        colors: [],
    });

    const updateFullViewParams = (params) => {
        setFullViewParams(params);
    }

    useEffect(() => {
        const updatedSearchParams = new URLSearchParams();
        updatedSearchParams.set("type", fractalType);
        updatedSearchParams.set("constant_x", fractalConstantX);
        updatedSearchParams.set("constant_y", fractalConstantY);
        updatedSearchParams.set("center_x", fractalCenterX);
        updatedSearchParams.set("center_y", fractalCenterY);
        updatedSearchParams.set("scale", fractalScale);
        updatedSearchParams.set("iterations", fractalIterations);
        updatedSearchParams.set("samples", fractalSamples);
        updatedSearchParams.set("render_width", fractalWidth);
        updatedSearchParams.set("render_height", fractalHeight);

        window.history.pushState({}, '', `?${updatedSearchParams.toString()}`);
    }, []);

    return <FractalContext.Provider value={{
        fullViewParams: fullViewParams,
    }}>
        <FractalUpdateContext.Provider value={{
            updateFullViewParams: updateFullViewParams,
        }}>
            { children }
        </FractalUpdateContext.Provider>
    </FractalContext.Provider>
}