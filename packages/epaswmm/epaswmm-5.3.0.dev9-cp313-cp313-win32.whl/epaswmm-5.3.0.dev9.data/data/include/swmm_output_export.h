
#ifndef EXPORT_SWMM_OUTPUT_API_H
#define EXPORT_SWMM_OUTPUT_API_H

#ifdef SHARED_EXPORTS_BUILT_AS_STATIC
#  define EXPORT_SWMM_OUTPUT_API
#  define SWMM_OUTPUT_NO_EXPORT
#else
#  ifndef EXPORT_SWMM_OUTPUT_API
#    ifdef swmm_output_EXPORTS
        /* We are building this library */
#      define EXPORT_SWMM_OUTPUT_API __declspec(dllexport)
#    else
        /* We are using this library */
#      define EXPORT_SWMM_OUTPUT_API __declspec(dllimport)
#    endif
#  endif

#  ifndef SWMM_OUTPUT_NO_EXPORT
#    define SWMM_OUTPUT_NO_EXPORT 
#  endif
#endif

#ifndef SWMM_OUTPUT_DEPRECATED
#  define SWMM_OUTPUT_DEPRECATED __declspec(deprecated)
#endif

#ifndef SWMM_OUTPUT_DEPRECATED_EXPORT
#  define SWMM_OUTPUT_DEPRECATED_EXPORT EXPORT_SWMM_OUTPUT_API SWMM_OUTPUT_DEPRECATED
#endif

#ifndef SWMM_OUTPUT_DEPRECATED_NO_EXPORT
#  define SWMM_OUTPUT_DEPRECATED_NO_EXPORT SWMM_OUTPUT_NO_EXPORT SWMM_OUTPUT_DEPRECATED
#endif

/* NOLINTNEXTLINE(readability-avoid-unconditional-preprocessor-if) */
#if 0 /* DEFINE_NO_DEPRECATED */
#  ifndef SWMM_OUTPUT_NO_DEPRECATED
#    define SWMM_OUTPUT_NO_DEPRECATED
#  endif
#endif

#endif /* EXPORT_SWMM_OUTPUT_API_H */
