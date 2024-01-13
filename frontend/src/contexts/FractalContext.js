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
    const fractalParams = {
        type: query.get("type") || Constants.DEFAULT_FULL_VIEW_PARAMS.type,
        power: query.get("power") || Constants.DEFAULT_FULL_VIEW_PARAMS.power,
        constant: {
            x: query.get("constant_x") || Constants.DEFAULT_FULL_VIEW_PARAMS.constant_x,
            y: query.get("constant_y") || Constants.DEFAULT_FULL_VIEW_PARAMS.constant_y,
        },
        center: {
             x: query.get("center_x") || Constants.DEFAULT_FULL_VIEW_PARAMS.center_x,
             y: query.get("center_y") || Constants.DEFAULT_FULL_VIEW_PARAMS.center_y,
        },
        scale: query.get("scale") || Constants.DEFAULT_FULL_VIEW_PARAMS.scale,
        iterations: query.get("iterations") || Constants.DEFAULT_FULL_VIEW_PARAMS.iterations,
        samples: query.get("samples") || Constants.DEFAULT_FULL_VIEW_PARAMS.samples,
        dimensions: {
            width: query.get("render_width") || Constants.DEFAULT_FULL_VIEW_PARAMS.dimensions.width,
            height: query.get("render_height") || Constants.DEFAULT_FULL_VIEW_PARAMS.dimensions.height,
        },
        colors: [],
    };

    const [fullViewParams, setFullViewParams] = useState({
        type: fractalParams.type,
        power: Number(fractalParams.power),
        constant: { x: Number(fractalParams.constant.x), y: Number(fractalParams.constant.y) },
        center: { x: Number(fractalParams.center.x), y: Number(fractalParams.center.y) },
        scale: Number(fractalParams.scale),
        iterations: Number(fractalParams.iterations),
        samples: Number(fractalParams.samples),
        dimensions: {
            width: Number(fractalParams.dimensions.width),
            height: Number(fractalParams.dimensions.height),
        },
        colors: [],
    });

    const updateWindowParams = (params) => {
        const updatedSearchParams = new URLSearchParams();
        updatedSearchParams.set("type", params?.type);
        if (params?.type === "julia") updatedSearchParams.set("power", params?.power);
        updatedSearchParams.set("constant_x", params?.constant?.x);
        updatedSearchParams.set("constant_y", params?.constant?.y);
        updatedSearchParams.set("center_x", params?.center?.x);
        updatedSearchParams.set("center_y", params?.center?.y);
        updatedSearchParams.set("scale", params?.scale);
        updatedSearchParams.set("iterations", params?.iterations);
        updatedSearchParams.set("samples", params?.samples);
        updatedSearchParams.set("render_width", params?.dimensions?.width);
        updatedSearchParams.set("render_height", params?.dimensions?.height);

        window.history.pushState({}, '', `?${updatedSearchParams.toString()}`);
    }

    const updateFullViewParams = (params) => {
        setFullViewParams(params);
        updateWindowParams(params);
    }

    useEffect(() => {
        updateWindowParams(fractalParams);
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