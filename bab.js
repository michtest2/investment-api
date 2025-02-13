export const isAuthenticated = CatchAsyncError(async (req: Request, res: Response, next: NextFunction) => {
    const access_token = req.cookies.access_token as string;
  
    if (!access_token) {
      return next(new ErrorHandler("Please login to access this resource", 400));
    }
  
    const decoded = jwt.decode(access_token) as JwtPayload;
  
    if (!decoded) {
      return next(new ErrorHandler("access token is not valid", 400));
    }
  
    // check if the access token is expired
    if (decoded.exp && decoded.exp <= Date.now() / 1000) {
      try {
        await updateAccessToken(req, res, next);
      } catch (error) {
        return next(error);
      }
    } else {
      const user = await redis.get(decoded.id);
  
      if (!user) {
        return next(new ErrorHandler("Please login to access this resource", 400));
      }
  
      req.user = JSON.parse(user);
  
      next();
    }
  });