def task_qa(func, *args, **kwargs):
    try:
        result = func(*args, **kwargs)
        return {'success': True, **result}
    except Exception as e:
        return {'success': False, 'Error': str(e)}
    except ValueError as ve:
        return {'success': False, 'Error': str(ve)}
    except KeyError as ke:
        return {'success': False, 'Error': str(ke)}
    except TypeError as te:
        return {'success': False, 'Error': str(te)}
    except AttributeError as ae:
        return {'success': False, 'Error': str(ae)}
    except IndexError as ie:
        return {'success': False, 'Error': str(ie)}
    except ZeroDivisionError as zde:
        return {'success': False, 'Error': str(zde)}
    except NameError as ne:
        return {'success': False, 'Error': str(ne)}
    except ImportError as ie:
        return {'success': False, 'Error': str(ie)}
    except FileNotFoundError as fne:
        return {'success': False, 'Error': str(fne)}
    except PermissionError as pe:
        return {'success': False, 'Error': str(pe)}
    except NotImplementedError as nie:
        return {'success': False, 'Error': str(nie)}
    except AssertionError as ae:
        return {'success': False, 'Error': str(ae)}
    except KeyboardInterrupt as ki:
        return {'success': False, 'Error': str(ki)}
    except RuntimeError as re:
        return {'success': False, 'Error': str(re)}